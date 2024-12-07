import pandas as pd
import os
import re


root_folder = r"D:\IIT\2 Year\Diabetics"
categories = ['ALPHA GLUCO','SULFON','THIAZOL']

combined_data = pd.DataFrame()

def extract_dosage(Item_Name):

    match = re.search(r'(\d+(\.\d+)?MG)', str(Item_Name))
    if match:
        return match.group(0)
    return None


# Process each medicine category (subfolder)
for category in categories:
    # Construct the path to the subfolder
    category_folder = os.path.join(root_folder, category)

    # Loop through each file in the subfolder
    for file in os.listdir(category_folder):
        if file.startswith('~$') or not file.endswith('.xlsx'):  # Skip temporary and non-Excel files
            continue

        file_path = os.path.join(category_folder, file)
        print(f"Processing file: {file_path}")  # Debug: Print the file being processed

        # Extract the date from the file name (e.g., '2.24' from '2.24.xlsx')
        file_date = os.path.splitext(file)[0]

        try:
             #Read the Excel File
             data = pd.read_excel(file_path)

             # Handle empty first row
             if data.iloc[0].isnull().all():
                 data = pd.read_excel(file_path, header=1)

             #Handle empty first row
                 # Normalize column names
                 data.columns = data.columns.str.strip().str.lower()  # Lowercase and strip whitespace
                 print(f"Columns in file {file_path}: {data.columns.tolist()}")  # Debug: Print column names

                 #Check if the required columns exists

                 # Check if the required columns exist
                 if len(data.columns) < 5:
                     print(f"Not enough columns in {file_path}. Skipping this file.")
                     continue










