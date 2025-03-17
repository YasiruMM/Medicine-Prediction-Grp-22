import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta

# Load the dataset
file_path = "C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx"
df = pd.read_excel(file_path)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Aggregate sales data for each month (assuming daily data)
df_monthly = df.groupby(['Year', 'Month', 'Drug Name'])['Sales'].sum().reset_index()

# Create a proper Date index
df_monthly['Date'] = pd.to_datetime(df_monthly[['Year', 'Month']].assign(day=1))
df_monthly.set_index('Date', inplace=True)

# Select a specific drug for modeling (Example: 'GLIMEPRIDE')
drug_name = "GLIMEPRIDE"
df_drug = df_monthly[df_monthly["Drug Name"] == drug_name][["Sales"]]

# Plot the Sales Data
plt.figure(figsize=(10, 5))
plt.plot(df_drug, label='Historical Sales')
plt.title(f'Sales Trend for {drug_name}')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Check for Stationarity
from statsmodels.tsa.stattools import adfuller

result = adfuller(df_drug["Sales"].dropna())
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")
if result[1] > 0.05:
    print("Data is not stationary. Differencing is required.")
    df_drug["Sales_diff"] = df_drug["Sales"].diff().dropna()
else:
    print("Data is stationary. No differencing needed.")

# Determine ARIMA (p, d, q) using Auto ARIMA
auto_model = auto_arima(df_drug["Sales"].dropna(), seasonal=True, m=12,
                        stepwise=True, suppress_warnings=True)
print(f"Best ARIMA order: {auto_model.order}")

# Train ARIMA Model
p, d, q = auto_model.order
model = ARIMA(df_drug["Sales"], order=(p, d, q))
model_fit = model.fit()

# Forecast the next 6 months
future_steps = 6
future_dates = [df_drug.index[-1] + timedelta(days=30 * i) for i in range(1, future_steps + 1)]
forecast = model_fit.forecast(steps=future_steps)

# Convert forecast to DataFrame
forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Sales': forecast})
forecast_df.set_index('Date', inplace=True)

# Plot Predictions
plt.figure(figsize=(10, 5))
plt.plot(df_drug, label='Historical Sales')
plt.plot(forecast_df, label='Forecasted Sales', linestyle='dashed', color='red')
plt.title(f'Sales Forecast for {drug_name} (Next 6 Months)')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Save the results
output_file = "C:/Users/ASUS/OneDrive/Desktop/arima_predictions.xlsx"
forecast_df.to_excel(output_file)
print(f"Predictions saved successfully to {output_file}")
