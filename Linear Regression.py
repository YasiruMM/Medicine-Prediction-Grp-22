import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the dataset
input_file = 'train_data.xlsx'  # Replace with the actual file path
data = pd.read_excel(input_file)

# Convert 'Date' to datetime if not already
data['Date'] = pd.to_datetime(data['Date'])

# Select relevant features and target variable
features = ['Retail Price', 'Purchase Price', 'Mean Sale']  # Add other features if needed
target = 'Sales'

# Drop rows with missing values in selected columns
data = data.dropna(subset=features + [target])

# Split the data into features (X) and target (y)
X = data[features]
y = data[target]

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = LinearRegression()

# Train the model on the training set
model.fit(X_train, y_train)

# Get model coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R2): {r2}")

# Scatter plot of actual vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--')
plt.title("Actual vs Predicted Sales")
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.grid()
plt.show()

from sklearn.metrics import r2_score

# Calculate R-squared
r2 = r2_score(y_test, y_pred)
print(f"R-squared (R²): {r2:.2f}")
accuracy = r2 * 100
print(f"Model Accuracy: {accuracy:.2f}%")