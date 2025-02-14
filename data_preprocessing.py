import os
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

# Define folders for each drug
drugs_folders = {
    'Atorvastatin': r'C:/Users/ASUS/OneDrive/Desktop/ATOVASTINE',
    'Rosuvastatin': r'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin',
    'Simvastatin': r'C:/Users/ASUS/OneDrive/Desktop/SIMVAS'
}

# Function to extract dosage from drug name
def extract_dosage(item_name):
    match = re.search(r'(\d+(\.\d+)?\s*MG)', str(item_name).upper())
    if match:
        return match.group(0).replace(" ", "")
    return "Unknown"

# Function to process drug data
def process_drug_data(drug_name, folder_path):
    combined_data = pd.DataFrame()
    for file in os.listdir(folder_path):
        if file.startswith('~$') or not file.endswith('.xlsx'):
            continue
        file_path = os.path.join(folder_path, file)
        file_date = os.path.splitext(file)[0]
        try:
            data = pd.read_excel(file_path)
            if data.iloc[0].isnull().all():
                data = pd.read_excel(file_path, header=1)
            data.columns = data.columns.str.strip().str.lower()
            if len(data.columns) < 5:
                continue
            drug_col = data.iloc[:, 1] if drug_name == "Simvastatin" else data.iloc[:, 0]
            retail_price_col = data.iloc[:, 3] if drug_name == "Simvastatin" else data.iloc[:, 4]
            purchase_price_col = data.iloc[:, 2] if drug_name == "Simvastatin" else data.iloc[:, 3]
            sales_col = data.iloc[:, -1]
            dosage_col = drug_col.apply(extract_dosage)
            structured_data = pd.DataFrame({
                'Drug': drug_name,
                'Drug Name': drug_col,
                'Dosage': dosage_col,
                'Retail Price': retail_price_col,
                'Purchase Price': purchase_price_col,
                'Sales': sales_col,
                'Date': file_date,
            })
            combined_data = pd.concat([combined_data, structured_data], ignore_index=True)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    combined_data.to_excel(f'C:/Users/ASUS/OneDrive/Desktop/{drug_name}_Cleaned.xlsx', index=False)

# Process each drug
for drug, folder in drugs_folders.items():
    process_drug_data(drug, folder)

# Function to combine all drug data
def combine_all_drug_data():
    combined_data = pd.concat([
        pd.read_excel(f'C:/Users/ASUS/OneDrive/Desktop/{drug}_Cleaned.xlsx') for drug in drugs_folders
    ], ignore_index=True)
    combined_data['Disease Category'] = 'Cholesterol'
    combined_data.to_excel('C:/Users/ASUS/OneDrive/Desktop/Combined_Drug_Data.xlsx', index=False)
combine_all_drug_data()

# Function to clean missing values
def clean_missing_values(df):
    for col in ['Sales', 'Retail Price', 'Purchase Price']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Dosage'] = df.groupby('Drug Name')['Dosage'].transform(lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else 'Unknown')
    for col in ['Sales', 'Retail Price', 'Purchase Price']:
        df[col] = df.groupby('Drug Name')[col].transform(lambda x: x.fillna(x.median()))
    df['Profit Margin'] = df['Retail Price'] - df['Purchase Price']
    return df

# Clean missing values
combined_data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Combined_Drug_Data.xlsx')
combined_data = clean_missing_values(combined_data)
combined_data.to_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Processed.xlsx', index=False)

# Function to detect and handle outliers
def apply_winsorization(df, columns):
    for col in columns:
        lower, upper = df[col].quantile(0.05), df[col].quantile(0.95)
        df[col] = np.clip(df[col], lower, upper)
    return df

# Process outliers
processed_data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Processed.xlsx')
processed_data = apply_winsorization(processed_data, ['Retail Price', 'Purchase Price', 'Sales'])
processed_data.to_excel('C:/Users/ASUS/OneDrive/Desktop/one_Drug_Data_Winsorized.xlsx', index=False)
