"""This script implements the model training process."""

#Importing Python libraries
import logging

#Importing 3rd-party libraries
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

#Defining the logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#Defining the constants
DATA_PATH = 'https://raw.githubusercontent.com/ulabox/datasets/master/data/ulabox_orders_with_categories_partials_2017.csv'
DAY_NAMES = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
DAY_ORDER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def data_cleaning(ulabox_data):
    """Drops unnecessary columns in the data and makes the column values more readable."""

    #Drops the 'customer' and 'order' columns since they contain IDs.
    ulabox_data.drop(columns=['customer', 'order'], inplace=True)

    #Replaces the 'weekday' column values with readable names.
    ulabox_data['weekday'] = ulabox_data['weekday'].replace(DAY_NAMES)

    #Reorders the 'weekday' column values so that they are chronological.
    ulabox_data['weekday'] = ulabox_data['weekday'].astype('category').cat.reorder_categories(DAY_ORDER)

    #Converts the 'hour' column values to strings the represent readable hours.
    ulabox_data['hour'] = ulabox_data['hour'].astype(str).str.pad(2, fillchar='0') + 'h'

    return ulabox_data

def feature_engineering(ulabox_data):
    """Transforms the columns in the data so that they are ready for model fitting."""

    #Removes the '%' from the column names.
    ulabox_data.columns = ulabox_data.columns.astype(str).str.replace('%', '')

    #Converts the percentages in the response variables to probabilities.
    ulabox_data.loc[:,'Food':'Pets'] = ulabox_data.loc[:,'Food':'Pets']/100

    #Standardizes the numerical explanatory variables to be between 0 and 1.
    ulabox_data[['total_items', 'discount']] = MinMaxScaler().fit_transform(ulabox_data[['total_items', 'discount']])

    #One-hot encodes the categorical variables.
    #The base for 'weekday' is 'Mon' and the base for 'hour' is '00h'
    ulabox_data = pd.get_dummies(ulabox_data, drop_first=True)

    return ulabox_data

def data_splitting(ulabox_data):
    """Splitting the data into train and test sets for response and explanatory variables."""

    #Splitting the data into 80% train and 20% test sets.
    ulabox_train, ulabox_test = train_test_split(ulabox_data, test_size=0.2, random_state=100)

    #Re-indexing the train and test sets.
    ulabox_train.reset_index(drop=True, inplace=True)
    ulabox_test.reset_index(drop=True, inplace=True)

    #Getting the column names for the response variables.
    response_cols = ulabox_data.loc[:,'Food':'Pets'].columns

    #Separting the response variables from the train and test sets.
    response_train = ulabox_train[response_cols]
    response_test = ulabox_test[response_cols]

    #Getting the response variables corresponding to the maximum probabiliy from the train set.
    response_train_max = response_train.idxmax(axis='columns')

    #Separting the explanatory variables from the train and test sets.
    explanatory_train = ulabox_train.drop(columns=response_cols)
    explanatory_test = ulabox_test.drop(columns=response_cols)

    return response_cols, response_train, response_test, response_train_max, explanatory_train, explanatory_test

def creating_priors(response_train):
    """Creating prior probabilities required for the model fitting."""

    #Setting the mean of each response variable in the training set as priors.
    priors = list(response_train.mean().sort_index())

    #Adjusting the priors so they sum up to 1.
    priors[0] = priors[0] + (1 - sum(priors))

    return priors

def model_fitting(priors, explanatory_train, response_train_max):
    """Fitting the model on the training data."""

    #Setting the model object as a Multinomial Naive-Bayes Classifier with pre-determined priors.
    model = MultinomialNB(class_prior=priors)

    #Fitting the model object on the explanatory variables and maximum response variables from the train set.
    model.fit(explanatory_train, response_train_max)

    return model

def model_evaluation(model, explanatory_test, response_cols, response_test):
    """Evaluating the model on the testing data."""

    #Predicting the response variable probabilities based the explanatory variables from the test set.
    response_pred = pd.DataFrame(model.predict_proba(explanatory_test))

    #Setting the proper names for the response variable prediction columns.
    response_pred.columns = sorted(response_cols)

    #Evaluating the model based on the mean absolute error between response variables in the test set and the predictions.
    model_eval = abs(response_test - response_pred).mean()

    return model_eval

if __name__ == '__main__':

    #Data Reading
    ulabox_data = pd.read_csv(DATA_PATH)
    LOGGER.info('Read the data successfully.')

    #Data Cleaning
    ulabox_data = data_cleaning(ulabox_data)
    LOGGER.info('Cleaned the data successfully.')

    #Feature Engineering
    ulabox_data = feature_engineering(ulabox_data)
    LOGGER.info('Engineered the features successfully.')

    #Data Splitting
    response_cols, response_train, response_test, response_train_max, explanatory_train, explanatory_test = data_splitting(ulabox_data)
    LOGGER.info('Split the data successfully.')

    #Creating Priors
    priors = creating_priors(response_train)
    LOGGER.info('Created the priors successfully.')

    #Model Fitting
    model = model_fitting(priors, explanatory_train, response_train_max)
    LOGGER.info('Fit the model successfully.')

    #Model Evaluation
    model_eval = model_evaluation(model, explanatory_test, response_cols, response_test)
    LOGGER.info('Evaluated the model successfully.')
