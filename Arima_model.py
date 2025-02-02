import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pmdarima import auto_arima

# Load datasets with proper datetime parsing
input_file1 = 'train_data.xlsx'
input_file2 = 'test_data.xlsx'
train_data = pd.read_excel(input_file1, parse_dates=['Date'])
test_data = pd.read_excel(input_file2, parse_dates=['Date'])

# Ensure 'Date' is set as the index
train_data.set_index('Date', inplace=True)
test_data.set_index('Date', inplace=True)

# Remove duplicate dates by averaging
train_data = train_data.groupby(train_data.index).mean()
test_data = test_data.groupby(test_data.index).mean()

# Sort before setting frequency
train_data = train_data.sort_index().asfreq('ME', method='ffill')
test_data = test_data.sort_index().asfreq('ME', method='ffill')

# Check for missing values
print("Missing dates in train:", train_data.isnull().sum())
print("Missing dates in test:", test_data.isnull().sum())

# Auto ARIMA for best (p, d, q)
best_model = auto_arima(train_data['Sales'], seasonal=False, trace=True)
print("Best ARIMA Order:", best_model.order)

# Fit ARIMA model with best order
model = ARIMA(train_data['Sales'], order=best_model.order)
model_fit = model.fit()

# Forecasting
if len(test_data) > 0:
    predictions = model_fit.forecast(steps=len(test_data))
    predictions.index = test_data.index  # Align predictions with test index
else:
    predictions = model_fit.forecast(steps=6)
    print("Forecasted Sales for Next 6 Periods:")
    print(predictions)

# Evaluate Performance (only if test data is available)
if len(test_data) > 0:
    mae = mean_absolute_error(test_data['Sales'], predictions)
    rmse = np.sqrt(mean_squared_error(test_data['Sales'], predictions))
    print(f"ARIMA - Mean Absolute Error: {mae}")
    print(f"ARIMA - Root Mean Squared Error: {rmse}")

    # Plot predictions vs actual
    plt.figure(figsize=(10, 6))
    plt.plot(test_data.index, test_data['Sales'], label='Actual', color='blue')
    plt.plot(test_data.index, predictions, label='Predicted', color='red', linestyle='dashed')
    plt.title('ARIMA: Actual vs Predicted Sales')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()
