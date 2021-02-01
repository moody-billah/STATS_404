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
