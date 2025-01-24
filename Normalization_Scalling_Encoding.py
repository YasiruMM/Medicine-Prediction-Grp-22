import pandas as pd
from openpyxl.styles.builtins import output
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
import numpy as np

def preprocess_data(input_file, output_file):
    # Load the dataset
    data = pd.read_excel(input_file)

    # Debugging: Print columns in the file
    print(f"Processing file: {input_file}")
    print("Columns in the input file:", data.columns.tolist())

    # Ensure required columns are present
    required_columns = ['Drug', 'Date', 'Monthly Sales', 'Average Monthly Profit Margin', 'Retail Price', 'Purchase Price', 'Dosage']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"The input file is missing one or more required columns: {required_columns}")

    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    if data['Date'].isnull().any():
        print("Warning: Invalid dates found and coerced to NaT.")
        # Handle NaT rows or drop them as needed
        data = data.dropna(subset=['Date'])

    # Extract features from 'Date'
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year

    # Normalize/Scale Numeric Data
    numeric_columns = ['Retail Price', 'Purchase Price', 'Monthly Sales']
    scaler = MinMaxScaler()
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

    # One-Hot Encode Categorical Variables
    categorical_columns = ['Drug', 'Dosage']
    encoder = OneHotEncoder(sparse_output=False, drop='first')  # Drop first to avoid dummy variable trap
    encoded_columns = encoder.fit_transform(data[categorical_columns])
    encoded_columns_df = pd.DataFrame(
        encoded_columns,
        columns=encoder.get_feature_names_out(categorical_columns),
        index=data.index
    )
    data = pd.concat([data, encoded_columns_df], axis=1)

    # Drop original categorical columns
    data.drop(columns=categorical_columns, inplace=True)

    # Save preprocessed data
    data.to_excel(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")


input_file='C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'
output_file='C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Preprocessed.xlsx'

preprocess_data(input_file, output_file)