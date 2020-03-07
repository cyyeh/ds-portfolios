# House Prices: Advanced Regression Techniques

> Predict sales prices and practice feature engineering, RFs, and gradient boosting

source: https://www.kaggle.com/c/house-prices-advanced-regression-techniques

## Description 

With 79 explanatory variables describing (almost) every aspect of residential homes in Ames, Iowa, this competition challenges you to predict the final price of each home.

**Practice Skills**
- Creative feature engineering 
- Advanced regression techniques like random forest and gradient boosting

## Evaluation

**Goal**

It is your job to predict the sales price for each house. For each Id in the test set, you must predict the value of the SalePrice variable. 

**Metric**

Submissions are evaluated on Root-Mean-Squared-Error (RMSE) between the logarithm of the predicted value and the logarithm of the observed sales price. (Taking logs means that errors in predicting expensive houses and cheap houses will affect the result equally.)

**Submission File Format**

See `sample_submission.csv`

## To Do List

- [ ] Implement the baseline model
- [ ] Try different regression models
- [ ] Apply cross-validation techniques
- [ ] Feature engineering
- [ ] Use pipeline
- [ ] Auto-sklearn