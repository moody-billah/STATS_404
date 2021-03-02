# Business Use Case: Ulabox

## Statement of Problem:

Ulabox needs to find a strategy to increase the revenue generated from its existing customers.

## Client:

Ulabox is an online grocery startup in Spain with €1 million in monthly revenue.

## Key Business Question:

Is there a way to analyze customer buying patterns so that Ulabox can better target the product recommendations on their app and website?

## Data Sources:

*The Ulabox Online Supermarket Dataset 2017, accessed from https://www.github.com/ulabox/datasets*

This dataset contains 30,000 orders from around 10,000 unique customers.

## Business Impact of Work:

Ulabox currently has €1 million in monthly revenue from about 10,000 customers, which means that each customer spends on average €100 per month.

They assume that better targeted product recommendations will lead to customers spending more money resulting in higher revenue. For example, if each customer spends on average €20 more per month, monthly revenue will increase by €200,000.

## How will Ulabox use the model to make decisions:

Ulabox currently has 8 categories of products. The model will try to predict the share of each category a customer will purchase when they start shopping.

Those predictions will be used the determine the share of product recommendations for each category. For example, if a customer is predicted to have 50% of their purchase in the Fresh category, 50% of their product recommendations will also be in the Fresh category.

## Metric to be monitored to see if the model is promising:

The predicted share of product categories will be compared with the actual share of product categories to evaluate the effectiveness of this model.

## Methodology:

In this project, the goal of the model is to predict the share of customer spending in each category for a new order. The dataset already contains the share per category of all existing orders, as well as some additional independent variables. 80% of the dataset is used for training the model and the remaining 20% is used for testing (HW3_Modeling, cell [6]).

The Naïve Bayes classifier was chosen as the model, which uses Bayesian inferencing to output probabilities of each class in the outcome variable. This is appropriate for the business question because the probabilities can represent the expected share per category. The ‘Naïve’ part assumes that all the variables are independent of each other, which makes the computation easier.

The ‘naive_bayes’ package from ‘sklearn’ was used to build this model. Some basic feature engineering was done to prepare the data for modeling, which include converting response variables to probabilities, scaling continuous variables to be between 0 and 1, and one hot encoding categorical variables (HW3_Modeling, cells [3] – [5]). When training the model, the multinomial distribution was used since most of the features were discrete. Two versions of the model were tested, one with prior probabilities updated based on the data, and another with fixed prior probabilities based the overall mean share per category (HW3_Modeling, cells [7], [12]). The loss function used to evaluate the model was the absolute mean error for each category (HW3_Modeling, cells [10], [15]).

The second version of the model with fixed priors was slightly better because the predictions were more balanced across categories. However, both versions of the were not very accurate in their overall predictions. This is mainly due to limitations in the dataset, since the explanatory variables did not have any strong relationship with the response variables. Although this model lacked accuracy, it can still be a starting point for answering the business question. If a model is already developed, it will be easier to add new data in the future to improve it, rather than rebuilding another model.

