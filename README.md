# DS_StackOver_Flow_Salary_Prediction-_-_Data_Exploration - URL: https://so-survey.herokuapp.com/
Working with Stack overflow survey data and building a simple salary prediction model and using data for exploration and visualization to gain insights into the data.

# Software Engineer Salary Estimator & Data Visualization: Project Overview
* Created a tool that estimates Software Engineer salaries (MAE ~ $ 27K) to help Software Engineers negotiate their income based on  various factors
  when they get a job.
* Downloaded data sets from surevey data on Stack-Overflow website for the years 2018,2019,2020 & 2021.
## Dataset 1 - Prediction Page
* Used the 2021 dataset to build the predictor model, since that would yield the most relevant results in terms of salary.
* Kept Years of experience, country and education level as final features for the model.
* Label encoded above features after cleaning text and numerical values.
* Optimized Linear,Decision Trees,Random Forest Regressor and XGBoost using GridsearchCV to reach the best model.
* Built a client facing API using Streamlit.
* Deployed the API on Heroku cloud platform.
## Dataset 2 - Explore Page
* Used the 2018,2019,2020 & 2021 dataset for data visualizxation and data exploration.
* I used data from above four years only, since there was some commonality in the information recieved during the survey.
* The website host data sets started from 2012, but it was difficult to align and extract data and features from those datasets.
* Finalized features for data exploration - Age,Gender,Sexual Orientation,Country,Languages workin with and desire to work with,education level,
  employment stsatus,salary and year.
* Had to input exchange rates for the year 2018 and calculate yearly salary from that.
* Rest of the datasets had annually calculated and converted salary amounts already present.
* Used matplotlib,Plotly and Seaborn for data visualization and exploratory analysis on all features and comibination of features.
* Deployed the API on Heroku cloud platform.

## Completed project on : https://so-survey.herokuapp.com/

## Code and Resources Used
**Python Version:** 3.9  
**Packages:** pandas, numpy, sklearn, matplotlib,plotly, seaborn,streamlit, json, pickle  
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  
**Salary predictor Github:** https://github.com/python-engineer/ml-app-salaryprediction
**STREAMLIT Dashboard deployment article:** https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku/
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2
**Youtube video-STREAMLIT app and machine learning model:** https://www.youtube.com/watch?v=xl0N7tHiwlw
**Youtube video-Heroku deployment:** https://www.youtube.com/watch?v=nJHrSvYxzjE


## Data Cleaning - Dataset 1
After downloading and reading the datasets, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

*	Parsed numeric data out of salary
*	Made columns for salary
*	Removed rows without salary
*	Parsed ages into age groups.
*	Shortened country catogories.
*	Pasred Sexual orientation, gender, education level and employment status into definite cataegories to work with.
*	Parsed languages to work with and working with so that they can be concatenated into a complete string.


## EDA


![alt text](pie.png "Plotly Pie chart")
