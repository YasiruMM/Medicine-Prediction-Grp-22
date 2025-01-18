import pandas as pd
import os
import re

# Define the main folders for each drug
drugs_folders = {
    'Atorvastatin': r'C:/Users/ASUS/OneDrive/Desktop/ATOVASTINE',
    'Simvastatin': r'C:/Users/ASUS/OneDrive/Desktop/SIMVAS',
    'Rosuvastatin': r'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin'
}

# Output folder for cleaned files
output_folder = r'C:\Path\To\CleanedFiles'
os.makedirs(output_folder, exist_ok=True)

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

        # Extract the date from the file name
        file_date = os.path.splitext(file)[0]

        try:
            data = pd.read_excel(file_path)

            if data.iloc[0].isnull().all():
                data = pd.read_excel(file_path, header=1)

            data.columns = data.columns.str.strip().str.lower()
            print(f"Columns in {file}: {data.columns.tolist()}")

            if len(data.columns) < 5:
                print(f"Not enough columns in {file}. Skipping.")
                continue

            drug_name_column = data.iloc[:, 0]
            dosage = drug_name_column.apply(extract_dosage)
            retail_price = data.iloc[:, 4]
            purchase_price = data.iloc[:, 3]
            sales = data.iloc[:, -1]

            structured_data = pd.DataFrame({
                'Drug': drug_name,
                'Drug Name': drug_name_column,
                'Dosage': dosage,
                'Retail Price': retail_price,
                'Purchase Price': purchase_price,
                'Sales': sales,
                'Date': file_date
            })

            combined_data = pd.concat([combined_data, structured_data], ignore_index=True)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    # Perform EDA
    print(f"EDA for {drug_name} data:")
    print(combined_data.describe())
    print(combined_data.isnull().sum())

    # Feature Engineering: Fill missing dosage with 'UNKNOWN'
    combined_data['Dosage'] = combined_data['Dosage'].fillna('UNKNOWN')

    # Remove rows with completely missing prices
    combined_data = combined_data.dropna(subset=['Retail Price', 'Purchase Price'], how='all')

    # Calculate Profit Margin
    combined_data['Profit Margin'] = combined_data['Retail Price'] - combined_data['Purchase Price']

    # Save cleaned data
    output_file = os.path.join(output_folder, f"cleaned_{drug_name.lower()}.xlsx")
    combined_data.to_excel(output_file, index=False)
    print(f"Cleaned data saved for {drug_name} at {output_file}")

# Process each drug folder
for drug, folder in drugs_folders.items():
    process_drug_data(drug, folder)
