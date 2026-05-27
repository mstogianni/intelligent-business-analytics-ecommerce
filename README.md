# Business Analytics and Forecasting System

An intelligent business analytics system for e-commerce applications, developed in Python.  
The project performs data preprocessing, business analytics, sales forecasting, and sales optimization recommendations through an interactive Streamlit web application.

## Features

- Data preprocessing and cleaning
- Business KPIs calculation
- Top categories, sub-categories, and products analysis
- Sales analysis by region, segment, and optionally country
- Monthly sales forecasting for the next 3 months
- ABC analysis for products and sub-categories
- Sales optimization recommendations
- Interactive CSV upload and column mapping through Streamlit

## Project Structure

- `app.py` - Streamlit web application
- `main.py` - local execution entry point
- `pipeline.py` - main analytics pipeline
- `data_utils.py` - data loading and cleaning
- `analytics.py` - analytics functions
- `forecasting.py` - forecasting functions
- `business_recommendations.py` - sales optimization recommendation engine
- `visualizations.py` - plotting functions
- `requirements.txt` - project dependencies

## Requirements

Install the required packages with:

```bash
pip install -r requirements.txt
```
Run the Application

To launch the Streamlit application:

streamlit run app.py
Input Data

The system supports CSV upload.
Users can either:

upload a CSV file using the expected structure
or upload their own CSV and map the required columns manually inside the application
Required fields
Order Date
Sales
Optional fields
Order ID
Ship Date
Customer ID
Segment
Country
Region
Category
Sub-Category
Product Name
Output

The system generates:

business KPIs
sales analysis tables and charts
monthly forecasting metrics
next 3 months sales forecast
ABC analysis
sales optimization recommendations
Technologies Used
Python
Pandas
NumPy
Matplotlib
Scikit-learn
Statsmodels
Mlxtend
Streamlit
Academic Context

This project was developed as part of a thesis on the design and implementation of an intelligent business analytics system for e-commerce applications using Python.
