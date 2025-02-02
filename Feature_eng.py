import pandas as pd
import re

# Function to standardize drug names by removing dosage information
def standardize_drug_name(drug_name):
    if not isinstance(drug_name, str):
        return 'Unknown'  # Handle non-string or missing drug names gracefully
    return re.sub(r'\s*\d+\s*MG', '', drug_name, flags=re.IGNORECASE).strip()

def feature_engineering(input_file, output_file):
    # Load the dataset
    data = pd.read_excel(input_file)

    # Ensure required columns are present
    required_columns = ['Disease Category', 'Drug Category', 'Drug Name', 'Dosage','Retail Price', 'Purchase Price', 'Sales', 'Date', 'Mean Sales','CV','Buffer Percentage','Buffer Stock']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"The input file is missing one or more required columns: {required_columns}")

    # --- Step 1: Standardize Drug Names ---
    data['Standardized Drug Name'] = data['Drug Name'].apply(standardize_drug_name)
    data['Drug Identifier'] = data['Standardized Drug Name'] + ' ' + data['Dosage'].astype(str)
    data['Drug Name'] = data['Drug Identifier']
    data.drop(columns=['Standardized Drug Name', 'Drug Identifier'], inplace=True)

    # --- Step 2: Extract Date-Based Features ---
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    # data['Day_of_Week'] = pd.to_datetime(data['Date']).dt.dayofweek
    # data['Is_Weekend'] = data['Day_of_Week'].isin([5, 6]).astype(int)

    # --- Step 3: Generate Lag-Based Features ---
    data['Lag_1'] = data.groupby('Drug Name')['Sales'].shift(1)
    data['Lag_2'] = data.groupby('Drug Name')['Sales'].shift(2)

    # --- Step 4: Calculate Mean Sales ---
    data['Mean Sale'] = data.groupby(['Drug Name'])['Sales'].transform('mean')

    # --- Step 5: Create Aggregate Features ---
    # category_sales = data.groupby('Disease Category')['Sales'].agg(['sum', 'mean']).reset_index()
    # category_sales.rename(columns={'sum': 'Total_Category_Sales', 'mean': 'Avg_Category_Sales'}, inplace=True)
    # data = pd.merge(data, category_sales, on='Disease Category', how='left')

    # --- Step 6: Retain relevant columns ---
    final_columns = ['Disease Category', 'Drug Category', 'Drug Name', 'Dosage','Retail Price', 'Purchase Price', 'Sales', 'Date','Month',  'Lag_1', 'Lag_2','Mean Sale','CV','Buffer Percentage','Buffer Stock']
    data = data[final_columns]

    # --- Step 7: Save the processed data ---
    data.to_excel(output_file, index=False)
    print(f"Feature engineering completed and saved to {output_file}")

# File paths for input and output
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Final_combined_data.xlsx'
output_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'

# Perform feature engineering
feature_engineering(input_file, output_file)
