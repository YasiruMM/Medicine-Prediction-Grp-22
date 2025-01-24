import pandas as pd
import os

# Define the output file path
output_combined_path = r'C:/Users/ASUS/OneDrive/Desktop/Combined_Drug_Data.xlsx'

# Function to add additional columns
def add_additional_columns(df, drug_name, disease_category):
    df['Drug Name'] = df['Drug Name'].str.strip()
    df['Disease Category'] = disease_category

    # Reorder columns to make 'Disease Category' the first column
    column_order = ['Disease Category'] + [col for col in df.columns if col != 'Disease Category']
    df = df[column_order]

    return df

# Function to combine all drug data
def combine_all_drug_data():
    combined_data = pd.DataFrame()

    # Process each drug's cleaned data
    # For Atorvastatin, Rosuvastatin, and Simvastatin, we have to load the cleaned data
    atorvastatin_data = pd.read_excel(r'C:/Users/ASUS/OneDrive/Desktop/Atorvastatin_Cleaned.xlsx', sheet_name='Atorvastatin')
    rosuvastatin_data = pd.read_excel(r'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin_Cleaned.xlsx', sheet_name='Rosuvastatin')
    simvastatin_data = pd.read_excel(r'C:/Users/ASUS/OneDrive/Desktop/Cleaned_Simvastatin_Data.xlsx', sheet_name='Simvastatin')

    # Add Disease Category and Drug Category to each dataset
    atorvastatin_data = add_additional_columns(atorvastatin_data, 'Atorvastatin', 'Cholesterol')
    rosuvastatin_data = add_additional_columns(rosuvastatin_data, 'Rosuvastatin', 'Cholesterol')
    simvastatin_data = add_additional_columns(simvastatin_data, 'Simvastatin', 'Cholesterol' )

    # Combine all data into one DataFrame
    combined_data = pd.concat([atorvastatin_data, rosuvastatin_data, simvastatin_data], ignore_index=True)

    # Save the combined data to Excel
    combined_data.to_excel(output_combined_path, index=False, sheet_name='Combined Data')
    print(f"Combined data saved at {output_combined_path}")

# Run the function to combine data
combine_all_drug_data()

# Perform basic EDA on the combined data
combined_data = pd.read_excel(output_combined_path, sheet_name='Combined Data')
print("EDA for Combined Drug Data:")

print(combined_data.describe(include='all'))
print(combined_data.isnull().sum())
