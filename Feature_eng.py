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
    required_columns = [
        'Disease Category', 'Drug', 'Drug Name', 'Dosage',
        'Retail Price', 'Purchase Price', 'Sales', 'Date'
    ]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"The input file is missing one or more required columns: {required_columns}")

    # --- Step 1: Standardize Drug Names ---
    data['Standardized Drug Name'] = data['Drug Name'].apply(standardize_drug_name)

    # Create a unique identifier for drugs by combining standardized name and dosage
    data['Drug Identifier'] = data['Standardized Drug Name'] + ' ' + data['Dosage'].astype(str)

    # Update 'Drug Name' column with the combined identifier
    data['Drug Name'] = data['Drug Identifier']

    # Drop temporary columns
    data.drop(columns=['Standardized Drug Name', 'Drug Identifier'], inplace=True)

    # --- Step 2: Convert 'Date' column to numeric format if necessary ---
    # (Skipping datetime conversion here based on the provided structure, but this can be added if needed)

    # --- Step 3: Calculate Mean Sale ---
    # Group by Drug and Date, and compute the mean sales
    mean_sales = data.groupby(['Drug Name', 'Date'])['Sales'].mean().reset_index()
    mean_sales.rename(columns={'Sales': 'Mean Sale'}, inplace=True)

    # Merge mean sales back into the main dataset
    data = pd.merge(data, mean_sales, on=['Drug Name', 'Date'], how='left')

    # --- Step 4: Retain relevant columns ---
    final_columns = [
        'Disease Category', 'Drug', 'Drug Name', 'Dosage',
        'Retail Price', 'Purchase Price', 'Sales', 'Date', 'Mean Sale'
    ]
    data = data[final_columns]

    # --- Step 5: Save the processed data ---
    data.to_excel(output_file, index=False)
    print(f"Feature engineering completed and saved to {output_file}")


# File paths for input and output
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Winsorized.xlsx'
output_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'

# Perform feature engineering
feature_engineering(input_file, output_file)
