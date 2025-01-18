import os
import pandas as pd
import re

# Folder path for Simvastatin data
folder_path = r'C:/Users/ASUS/OneDrive/Desktop/SIMVAS'

# Initialize an empty DataFrame to store cleaned data
combined_data = pd.DataFrame()

# Function to extract dosage from the Drug Name
def extract_dosage(item_name):
    match = re.search(r'(\d+(\.\d+)?MG)', str(item_name))  # Captures dosages like "5MG" or "2.5MG"
    if match:
        return match.group(0)
    return None

# Function to clean and process Simvastatin data
def process_simvastatin_data():
    global combined_data

    for file in os.listdir(folder_path):
        if file.startswith('~$') or not file.endswith('.xlsx'):  # Skip temporary or non-Excel files
            continue

        file_path = os.path.join(folder_path, file)
        print(f"Processing file: {file_path}")

        # Extract the date from the file name
        file_date = os.path.splitext(file)[0]

        try:
            # Read the Excel file
            data = pd.read_excel(file_path)

            # Handle empty first row
            if data.iloc[0].isnull().all():
                data = pd.read_excel(file_path, header=1)

            # Normalize column names
            data.columns = data.columns.str.strip().str.lower()
            print(f"Columns in {file}: {data.columns.tolist()}")

            # Check if there are sufficient columns
            if len(data.columns) < 5:
                print(f"Not enough columns in {file}. Skipping.")
                continue

            # Extract relevant columns
            drug_name = data.iloc[:, 1]  # First column: Drug Name
            retail_price = data.iloc[:, 3]  # 5th column: Retail Price
            purchase_price = data.iloc[:, 2]  # 4th column: Purchase Price
            sales = data.iloc[:, -1]  # Last column: Sales

            # Extract dosage from the Drug Name
            dosage = drug_name.apply(extract_dosage)

            # Create a structured DataFrame
            structured_data = pd.DataFrame({
                'Drug': 'Simvastatin',
                'Drug Name': drug_name,
                'Dosage': dosage,
                'Retail Price': retail_price,
                'Purchase Price': purchase_price,
                'Sales': sales,
                'Date': file_date
            })

            # Remove rows where 'Drug Name' contains "Item Code" or is NaN
            structured_data = structured_data[~structured_data['Drug Name'].str.contains('Item Code', na=False)]
            structured_data = structured_data.dropna(subset=['Drug Name'])

            # Fill missing dosage with "Unknown"
            structured_data['Dosage'] = structured_data['Dosage'].fillna('Unknown')

            # Remove rows where all key numeric columns are zero
            structured_data = structured_data[
                ~((structured_data['Retail Price'] == 0) &
                  (structured_data['Purchase Price'] == 0) &
                  (structured_data['Sales'] == 0))
            ]

            # Calculate Profit Margin
            structured_data['Retail Price'] = pd.to_numeric(structured_data['Retail Price'], errors='coerce')
            structured_data['Purchase Price'] = pd.to_numeric(structured_data['Purchase Price'], errors='coerce')
            structured_data['Profit Margin'] = structured_data['Retail Price'] - structured_data['Purchase Price']

            # Append to the combined DataFrame
            combined_data = pd.concat([combined_data, structured_data], ignore_index=True)

        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue

    # Save the cleaned data to an Excel file
    output_path = r'C:/Users/ASUS/OneDrive/Desktop/Cleaned_Simvastatin_Data.xlsx'
    combined_data.to_excel(output_path, index=False, sheet_name='Simvastatin')
    print(f"Cleaned data saved to {output_path}")

# Run the cleaning and EDA process
if __name__ == "__main__":
    process_simvastatin_data()

    # Perform basic EDA
    print("EDA for Simvastatin data:")
    print(combined_data.describe(include='all'))  # Statistical summary
    print(combined_data.isnull().sum())  # Missing values
