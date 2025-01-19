import pandas as pd
import os
import re

# Define the main folders for each drug
drugs_folders = {
    'Atorvastatin': r'C:/Users/ASUS/OneDrive/Desktop/ATOVASTINE',
    'Rosuvastatin': r'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin'
}


# Function to extract dosage from drug name
def extract_dosage(item_name):
    match = re.search(r'(\d+(\.\d+)?MG)', str(item_name), re.IGNORECASE)
    if match:
        return match.group(0).upper()
    return None


# Function to clean and structure data for a given folder
def process_drug_data(drug_name, folder_path):
    combined_data = pd.DataFrame()

    for file in os.listdir(folder_path):
        if file.startswith('~$') or not file.endswith('.xlsx'):
            continue

        file_path = os.path.join(folder_path, file)
        print(f"Processing file: {file_path}")

        file_date = os.path.splitext(file)[0]

        try:
            data = pd.read_excel(file_path)

            # Handle empty first row
            if data.iloc[0].isnull().all():
                data = pd.read_excel(file_path, header=1)

            data.columns = data.columns.str.strip().str.lower()
            print(f"Columns in {file}: {data.columns.tolist()}")

            if len(data.columns) < 5:
                print(f"Not enough columns in {file}. Skipping this file.")
                continue

            # Extract necessary data
            drug_col = data.iloc[:, 0]
            retail_price_col = data.iloc[:, 4]
            purchase_price_col = data.iloc[:, 3]
            sales_col = data.iloc[:, -1]

            # Extract dosage
            dosage_col = drug_col.apply(extract_dosage)

            # Create structured DataFrame
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
            continue

    # Convert price columns to numeric
    combined_data['Retail Price'] = pd.to_numeric(combined_data['Retail Price'], errors='coerce')
    combined_data['Purchase Price'] = pd.to_numeric(combined_data['Purchase Price'], errors='coerce')

    # Handle missing prices
    combined_data['Retail Price'].fillna(0, inplace=True)
    combined_data['Purchase Price'].fillna(0, inplace=True)

    # Calculate Profit Margin
    combined_data['Profit Margin'] = combined_data['Retail Price'] - combined_data['Purchase Price']

    # EDA
    print(f"EDA for {drug_name} data:")
    print(combined_data.describe(include='all'))
    print(combined_data.isnull().sum())

    # Save cleaned data
    output_path = f'C:/Users/ASUS/OneDrive/Desktop/{drug_name}_Cleaned.xlsx'
    combined_data.to_excel(output_path, index=False, sheet_name=f'{drug_name}')
    print(f"Cleaned data saved for {drug_name} at {output_path}")


# Process each drug folder
for drug, folder in drugs_folders.items():
    process_drug_data(drug, folder)


