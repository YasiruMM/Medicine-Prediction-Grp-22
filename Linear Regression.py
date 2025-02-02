import pandas as pd
import numpy as np  # Import NumPy for square root function
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

# Load the encoded dataset
encoded_data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured_Encoded.xlsx')

# Define features (X) and target (y)
X = encoded_data.drop(columns=['Sales'])  # Drop the target column
y = encoded_data['Sales']  # Target column (continuous variable)

# Handle missing values (Fill NaN with Mean)
imputer = SimpleImputer(strategy="mean")
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Predictions
lr_predictions = lr_model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, lr_predictions)
mse = mean_squared_error(y_test, lr_predictions)
rmse = np.sqrt(mse)  # Compute RMSE manually
r2 = r2_score(y_test, lr_predictions)

# Print Results
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)  # RMSE fixed!
print("R-squared (R²):", r2)