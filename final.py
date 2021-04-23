"""This script implements the model scoring process."""

#Importing Python libraries.
import logging
import json
from urllib.request import urlopen

#Importing 3rd-party libraries.
import joblib
import pandas as pd
from sklearn.naive_bayes import MultinomialNB

#Defining the logger.
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#Defining the input and output JSON files.
INPUT_JSON = "input_spec.json"
OUTPUT_JSON = "output_spec.json"

#Defining the AWS S3 bucket links.
SCALER_URL = urlopen("https://stats404-final-moody-billah.s3.amazonaws.com/minmax_scaler.json")
MODEL_URL = urlopen("https://stats404-final-moody-billah.s3.amazonaws.com/final_model.pkl")

#Defining the business case related constants.
INPUT_KEYS = ['total_items', 'discount%', 'weekday', 'hour']
OUTPUT_KEYS = ['Baby%', 'Beauty%', 'Drinks%', 'Food%', 'Fresh%', 'Health%', 'Home%', 'Pets%']
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
HOURS = ['00h', '01h', '02h', '03h', '04h', '05h', '06h', '07h', '08h', '09h', '10h', '11h', 
         '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h']

def read_input(INPUT_JSON):
    """Reads the input JSON file which must be in the same directory as this script."""

    #Reads the input JSON file.
    with open(INPUT_JSON) as file:
        input_spec = json.load(file)

    return input_spec

def input_validation(input_spec, INPUT_KEYS, WEEKDAYS, HOURS):
    """Validates the input values and throws an error if they are not compatible."""

    #Validates the keys in the input file.
    if (list(input_spec.keys()) == INPUT_KEYS) is False:
        raise ValueError('The input_spec.json file has incorrect keys. Key values should not be altered from the orginal.')

    #Validates the "total_items" value in the input file.
    if type(input_spec['total_items']) is not int:
        raise ValueError('The "total_items" value in the input_spec.json file must be an integer.')

    #Validates the "discount%" value in the input file.
    if input_spec['discount%'] > 100 or input_spec['discount%'] < 0:
        raise ValueError('The "discount%" value in the input_spec.json file must be between 0 and 100.')

    #Validates the "weekday" value in the input file.
    if input_spec['weekday'] not in WEEKDAYS:
        raise ValueError('The "weekday" value in the input_spec.json file must be in the format "Mon", "Tue", etc.')

    #Validates the "hour" value in the input file.
    if input_spec['hour'] not in HOURS:
        raise ValueError('The "hour" value in the input_spec.json file must be in the format "00h", "01h", etc up to a maximum of "23h".')

def input_conversion(input_spec, SCALER_URL):
    """Converts the input values so that they are appropriate for the model."""

    #Reads the scaling factor numbers from the AWS S3 bucket.
    scaler = json.loads(SCALER_URL.read())

    #Scales the "total_items" values to be between 0 and 1.
    total_items = (input_spec['total_items'] - scaler['total_items_min']) / (scaler['total_items_max'] - scaler['total_items_min'])

    #Scales the "discount" values to be between 0 and 1.
    discount = (input_spec['discount%'] - scaler['discount%_min']) / (scaler['discount%_max'] - scaler['discount%_min'])

    #Adds a prefix to the "weekday" values.
    weekday = 'weekday_' + input_spec['weekday']

    #Adds a prefix to the "hour" values.
    hour = 'hour_' + input_spec['hour']

    return total_items, discount, weekday, hour

def feature_engineering(total_items, discount, weekday, hour, WEEKDAYS, HOURS):
    """Creates a feature dataset that is appropriate for the model input."""

    #Creates the features for the "weekday" values with "weekday_Mon" as the base.
    weekday_cols = ['weekday_' + i for i in WEEKDAYS]
    weekday_cols.remove('weekday_Mon')

    #Creates the features for the "hour" values with "'hour_00h" as the base.
    hour_cols = ['hour_' + i for i in HOURS]
    hour_cols.remove('hour_00h')

    #Creates a dataframe of zeros with all the necessary features.
    input_cols = ['total_items', 'discount'] + weekday_cols + hour_cols
    input_df = pd.DataFrame(columns=input_cols)
    input_df.loc[0] = 0

    #Populates the dataframe with the appropriate "total_items" values.
    input_df['total_items'] = total_items

    #Populates the dataframe with the appropriate "discount" values.
    input_df['discount'] = discount

    #Populates the dataframe with the appropriate "weekday" values.
    if weekday in weekday_cols:
        input_df[weekday] = 1

    #Populates the dataframe with the appropriate "hour" values.
    if hour in hour_cols:
        input_df[hour] = 1

    return input_df

def model_scoring(input_df, MODEL_URL):
    """Scores the model using the feature dataset to make predictions."""

    #Reads the model object from the AWS S3 bucket.
    model = joblib.load(MODEL_URL)

    #Makes predictions using the model object.
    model_pred = model.predict_proba(input_df).tolist()[0]

    return model_pred

def output_conversion(model_pred, OUTPUT_KEYS):
    """Converts the predictions into a readable format required for the output JSON."""

    #Converts the prediction values to represent whole number percentages.
    output_values = [round(i*100) for i in model_pred]

    #Matches the prediction values with the appropriate response variable names.
    output_spec = dict(zip(OUTPUT_KEYS, output_values))

    return output_spec

def export_ouput(output_spec, OUTPUT_JSON):
    """Exports the output JSON file in the same directory as this script."""

    #Exports the predictions into the output JSON file.
    with open(OUTPUT_JSON, 'w') as file:
        json.dump(output_spec, file, indent=1)

if __name__ == '__main__':

    #Read Input
    input_spec = read_input(INPUT_JSON)
    LOGGER.info('Read the ' + INPUT_JSON + ' file successfully.')

    #Input Validation
    input_validation(input_spec, INPUT_KEYS, WEEKDAYS, HOURS)
    LOGGER.info('The input values were validated successfully.')

    #Input Conversion
    total_items, discount, weekday, hour = input_conversion(input_spec, SCALER_URL)
    LOGGER.info('The input values were converted successfully.')

    #Feature Engineering
    input_df = feature_engineering(total_items, discount, weekday, hour, WEEKDAYS, HOURS)
    LOGGER.info('The features needed for model input was created successfully.')

    #Model Scoring
    model_pred = model_scoring(input_df, MODEL_URL)
    LOGGER.info('The model made predictions successfully.')

    #Output Conversion
    output_spec = output_conversion(model_pred, OUTPUT_KEYS)
    LOGGER.info('The output predictions were converted successfully.')

    #Export Output
    export_ouput(output_spec, OUTPUT_JSON)
    LOGGER.info('Exported the ' + OUTPUT_JSON + ' file successfully.')
