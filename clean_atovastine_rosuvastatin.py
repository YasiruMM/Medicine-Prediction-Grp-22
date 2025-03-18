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
    """
    Extracts the dosage (in MG) from the drug name using regex.
    Handles cases like "5MG", "20 MG", or "2.5MG".
    """
    match = re.search(r'(\d+(\.\d+)?\s*MG)', str(item_name).upper())
    if match:
        return match.group(0).replace(" ", "")  # Remove any spaces in the result

    # If no "MG" is found, try to match standalone numbers like "05" or "10"
    match = re.search(r'\b\d+\b', str(item_name))
    if match:
        return f"{int(match.group(0))}MG"

    return "Unknown"  # If no match is found

# Function to clean and structure data for a given folder
def process_drug_data(drug_name, folder_path):
    """
    Reads all Excel files in the given folder, extracts relevant data, cleans it,
    calculates profit margin, and saves the structured data to a new Excel file.
    """
    combined_data = pd.DataFrame()

    # Iterate over all files in the folder
    for file in os.listdir(folder_path):
        # Ignore temporary or non-Excel files
        if file.startswith('~$') or not file.endswith('.xlsx'):
            continue

        file_path = os.path.join(folder_path, file)
        print(f"Processing file: {file_path}")

        # Extract the date from the filename (assuming filename is the date)
        file_date = os.path.splitext(file)[0]

        try:
            # Read the Excel file
            data = pd.read_excel(file_path)

            # Handle case where the first row is empty
            if data.iloc[0].isnull().all():
                data = pd.read_excel(file_path, header=1)

            # Clean column names (strip spaces and convert to lowercase)
            data.columns = data.columns.str.strip().str.lower()
            print(f"Columns in {file}: {data.columns.tolist()}")

            # Skip files with insufficient columns
            if len(data.columns) < 5:
                print(f"Not enough columns in {file}. Skipping this file.")
                continue

            # Remove 'Item Code' column if it's the first column
            if 'Item Code' in data.columns[0]:
                data = data.iloc[:, 1:]

            # Extract necessary data columns
            drug_col = data.iloc[:, 0]  # First column: Drug name
            retail_price_col = data.iloc[:, 4]  # Fifth column: Retail Price
            purchase_price_col = data.iloc[:, 3]  # Fourth column: Purchase Price
            sales_col = data.iloc[:, -1]  # Last column: Sales

            # Extract dosage information from the drug name
            dosage_col = drug_col.apply(extract_dosage)

            # Create a structured DataFrame with relevant columns
            structured_data = pd.DataFrame({
                'Drug': drug_name,
                'Drug Name': drug_col,
                'Dosage': dosage_col,
                'Retail Price': retail_price_col,
                'Purchase Price': purchase_price_col,
                'Sales': sales_col,
                'Date': file_date,
            })

            # Append structured data to the combined DataFrame
            combined_data = pd.concat([combined_data, structured_data], ignore_index=True)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    # Convert price columns to numeric values
    combined_data['Retail Price'] = pd.to_numeric(combined_data['Retail Price'], errors='coerce')
    combined_data['Purchase Price'] = pd.to_numeric(combined_data['Purchase Price'], errors='coerce')

    # Handle missing price values by filling them with 0
    combined_data['Retail Price'].fillna(0, inplace=True)
    combined_data['Purchase Price'].fillna(0, inplace=True)

    # Calculate profit margin (Retail Price - Purchase Price)
    combined_data['Profit Margin'] = combined_data['Retail Price'] - combined_data['Purchase Price']

    # Perform exploratory data analysis (EDA)
    print(f"EDA for {drug_name} data:")
    print(combined_data.describe(include='all'))  # Summary statistics
    print(combined_data.isnull().sum())  # Count of missing values

    # Save cleaned data to an Excel file
    output_path = f'C:/Users/ASUS/OneDrive/Desktop/{drug_name}_Cleaned.xlsx'
    combined_data.to_excel(output_path, index=False, sheet_name=f'{drug_name}')
    print(f"Cleaned data saved for {drug_name} at {output_path}")

# Process each drug folder
for drug, folder in drugs_folders.items():
    process_drug_data(drug, folder)
