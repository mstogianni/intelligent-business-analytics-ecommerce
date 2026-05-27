# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:55:49 2026

@author: fotev
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_monthly_forecast(monthly_summary, test_periods=6):
    monthly_sales = monthly_summary["Sales"].copy()
    train = monthly_sales.iloc[:-test_periods]
    test = monthly_sales.iloc[-test_periods:]
    model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
    y_pred = model.forecast(test_periods)
    mae = mean_absolute_error(test, y_pred)
    rmse = np.sqrt(mean_squared_error(test, y_pred))
    r2 = r2_score(test, y_pred)
    return train, test, y_pred, mae, rmse, r2

def forecast_next_3_months(monthly_summary):
    monthly_sales = monthly_summary["Sales"].copy()
    model = ExponentialSmoothing(monthly_sales, trend="add", seasonal="add", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
    forecast = model.forecast(3)
    forecast_df = pd.DataFrame({"PredictedSales": forecast})
    forecast_df.index.name = "YearMonth"
    return forecast_df