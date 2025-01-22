import pandas as pd

#Atorvastatin
# Load the uploaded Excel file to inspect the data for missing values
file_path = 'C:/Users/ASUS/OneDrive/Desktop/Atorvastatin_Cleaned.xlsx'
data = pd.ExcelFile(file_path)

# Load all sheets into a dictionary
sheets = {sheet_name: data.parse(sheet_name) for sheet_name in data.sheet_names}

# Analyze missing values for sheet
missing_values_report = {}
for sheet_name, df in sheets.items():
    missing_values_report[sheet_name] = df.isnull().sum()

# Display the report
print(missing_values_report)

#Rosuvastatin
file_path2= 'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin_Cleaned.xlsx'

data2 = pd.ExcelFile(file_path2)

sheets = {sheet_name: data2.parse(sheet_name) for sheet_name in data2.sheet_names}

missing_values_report2 = {}
for sheet_name, df in sheets.items():
    missing_values_report2[sheet_name] = df.isnull().sum()

print(missing_values_report2)

#Simvastatin
file_path3= 'C:/Users/ASUS/OneDrive/Desktop/Cleaned_Simvastatin_Data.xlsx'

data3 = pd.ExcelFile(file_path3)

sheets = {sheet_name: data3.parse(sheet_name) for sheet_name in data3.sheet_names}

missing_values_report3 = {}
for sheet_name, df in sheets.items():
    missing_values_report3[sheet_name] = df.isnull().sum()

print(missing_values_report3)

# Replace non-numeric values in relevant columns with NaN
for col in ['Sales', 'Retail Price', 'Purchase Price']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill missing values with imputation logic
df['Dosage'] = df.groupby('Drug Name')['Dosage'].transform(
    lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else x.fillna('Unknown')
)
df['Sales'] = df.groupby('Drug')['Sales'].transform(
    lambda x: x.fillna(x.median())
)
df['Retail Price'] = df.groupby('Drug Name')['Retail Price'].transform(
    lambda x: x.fillna(x.median())
)
df['Purchase Price'] = df.groupby('Drug Name')['Purchase Price'].transform(
    lambda x: x.fillna(x.median())
)

# Recalculate 'Profit Margin'
df['Profit Margin'] = df['Retail Price'] - df['Purchase Price']

# Check if there are any missing values left
print(df.isnull().sum())

