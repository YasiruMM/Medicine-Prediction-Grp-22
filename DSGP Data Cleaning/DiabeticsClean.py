import pandas as pd
import os
import re

# Define the main folder and subfolders (medicine categories)
main_folder = r'D:\IIT\2 Year\Diabetics'
medicine_categories = ['ALPHA GLUCO', 'SULFON', 'THIAZOL']

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Function to extract dosage from Drug Name (first column)
def extract_dosage(item_name):
    # Regex to find numbers (including decimals) followed by 'MG' (e.g., '2.5MG', '5MG')
    match = re.search(r'(\d+(\.\d+)?MG)', str(item_name))  # captures both integers and decimals followed by MG
    if match:
        return match.group(0)  # Return the matched dosage (e.g., '5MG' or '2.5MG')
    return None  # Return None if no dosage is found

# Process each medicine category (subfolder)
for category in medicine_categories:
    # Construct the path to the subfolder
    category_folder = os.path.join(main_folder, category)

    # Loop through each file in the subfolder
    for file in os.listdir(category_folder):
        if file.startswith('~$') or not file.endswith('.xlsx'):  # Skip temporary and non-Excel files
            continue

        file_path = os.path.join(category_folder, file)
        print(f"Processing file: {file_path}")  # Debug: Print the file being processed

        # Extract the date from the file name (e.g., '2.24' from '2.24.xlsx')
        file_date = os.path.splitext(file)[0]

        try:
            # Read the Excel file, skipping the first row (empty) and using the second row as header
            data = pd.read_excel(file_path, header=1)

            # Handle empty first row
            if data.isnull().all(axis=1).iloc[0]:
                data = pd.read_excel(file_path, header=2)  # Skip the first empty row and use the second as the header

            # Normalize column names
            data.columns = data.columns.str.strip().str.lower()  # Lowercase and strip whitespace
            print(f"Columns in file {file_path}: {data.columns.tolist()}")  # Debug: Print column names

            # Check if the required columns exist
            if len(data.columns) < 5:
                print(f"Not enough columns in {file_path}. Skip this file.")
                continue

            # Remove the last row (summary row)
            data = data.iloc[:-1, :]

            # Assume the first column always contains the drug name now
            drug_name = data.iloc[:, 0]  # First column: Drug Name

            # Extract the dosage directly from the Drug Name using the extract_dosage function
            dosage = drug_name.apply(extract_dosage)

            # Extract retail, purchase prices, and sales columns
            retail_price = data.iloc[:, 4]  # 5th column: Retail Price
            purchase_price = data.iloc[:, 3]  # 4th column: Purchase Price
            sales = data.iloc[:, -1]  # Last column: Sales

            # Create a structured DataFrame with the necessary columns
            structured_data = pd.DataFrame({
                'Disease Category': 'Diabetics',
                'Drug Category': category,
                'Drug Name': drug_name,
                'Dosage': dosage,  # Place the extracted dosage in the Dosage column
                'Retail Price': retail_price,  # Retail Price
                'Purchase Price': purchase_price,  # Purchase Price
                'Sales': sales,  # Sales
                'Date': file_date  # Use the extracted date
            })

            # Append structured data to the combined DataFrame
            combined_data = pd.concat([combined_data, structured_data], ignore_index=True)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

# After processing all files, save the combined data to an Excel file
output_path = r'D:\IIT\2 Year\Structured_Diabetics.xlsx'
combined_data.to_excel(output_path, index=False, sheet_name='Diabetics')

print(f"Data structured and saved successfully to the path {output_path}")