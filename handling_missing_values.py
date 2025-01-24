import pandas as pd


# Function to analyze missing values in all sheets of an Excel file
def analyze_missing_values(file_path):
    data = pd.ExcelFile(file_path)
    sheets = {sheet_name: data.parse(sheet_name) for sheet_name in data.sheet_names}

    # Generate missing value report
    missing_values_report = {
        sheet_name: df.isnull().sum() for sheet_name, df in sheets.items()
    }
    return sheets, missing_values_report


# Function to clean and impute missing values in a DataFrame
def clean_missing_values(df):
    # Replace non-numeric values in relevant columns with NaN
    for col in ['Sales', 'Retail Price', 'Purchase Price']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing 'Dosage' based on the mode for each 'Drug Name'
    df['Dosage'] = df.groupby('Drug Name')['Dosage'].transform(
        lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else x.fillna('Unknown')
    )

    # Impute missing numeric columns with median grouped by 'Drug Name'
    for col in ['Sales', 'Retail Price', 'Purchase Price']:
        df[col] = df.groupby('Drug Name')[col].transform(
            lambda x: x.fillna(x.median())
        )

    # Recalculate 'Profit Margin'
    df['Profit Margin'] = df['Retail Price'] - df['Purchase Price']

    return df


# Function to clean all sheets in an Excel file
def clean_excel_file(file_path, output_path):
    sheets, missing_report = analyze_missing_values(file_path)

    # Display the initial missing values report
    print(f"Initial Missing Values Report for {file_path}:")
    print(missing_report)

    # Clean each sheet
    cleaned_sheets = {}
    for sheet_name, df in sheets.items():
        cleaned_sheets[sheet_name] = clean_missing_values(df)

    # Save cleaned data back to Excel
    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, df in cleaned_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Check for remaining missing values after cleaning
    final_missing_report = {
        sheet_name: df.isnull().sum() for sheet_name, df in cleaned_sheets.items()
    }
    print(f"Final Missing Values Report for {output_path}:")
    print(final_missing_report)


# File paths
input_path='C:/Users/ASUS/OneDrive/Desktop/Combined_Drug_Data.xlsx'
output_path='C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Processed.xlsx'

# Process each file
clean_excel_file(input_path, output_path)
