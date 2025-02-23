import pandas as pd
import re

# Function to remove dosage information and standardize drug names
def standardize_drug_name(drug_name):
    """Removes dosage information and standardizes drug names."""
    if not isinstance(drug_name, str):
        return 'Unknown'
    return re.sub(r'\s*\d+\s*MG', '', drug_name, flags=re.IGNORECASE).strip()

# Function to apply feature engineering for drug demand forecasting
def feature_engineering(df):
    """Applies feature engineering for drug demand forecasting."""

    # Step 1: Standardize Drug Names
    df['Standardized Drug Name'] = df['Drug Name'].apply(standardize_drug_name)
    df['Drug Identifier'] = df['Standardized Drug Name'] + ' ' + df['Dosage'].astype(str)
    df['Drug Name'] = df['Drug Identifier']
    df.drop(columns=['Standardized Drug Name', 'Drug Identifier'], inplace=True)

    # Step 2: Convert Date Column to Date Format
    df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%m.%y', errors='coerce')
    df['Date'] = df['Date'].apply(lambda x: x.replace(day=1) if pd.notnull(x) else x)  # Set day to 1
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter

    # Step 3: Generate Lag-Based Features
    for lag in range(1, 3):  # Creating Lag_1 and Lag_2
        df[f'Lag_{lag}'] = df.groupby('Drug Name')['Sales'].shift(lag)

    # Step 4: Calculate Rolling Mean and Exponential Moving Average
    df['Rolling_Mean_3'] = df.groupby('Drug Name')['Sales'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df['EMA_3'] = df.groupby('Drug Name')['Sales'].transform(lambda x: x.ewm(span=3, adjust=False).mean())

    # Step 5: Compute Mean Sales
    df['Mean Sale'] = df.groupby(['Drug Name'])['Sales'].transform('mean')

    # Step 6: Compute Coefficient of Variation (CV) for Sales Variability
    df['CV'] = df.groupby(['Drug Name'])['Sales'].transform(lambda x: (x.std() / x.mean()) * 100)

    # Step 7: Calculate Buffer Stock Based on CV
    def buffer_percentage(cv):
        if cv <= 20:
            return 20
        elif 20 < cv <= 50:
            return 30
        else:
            return 50

    df['Buffer Percentage'] = df['CV'].apply(buffer_percentage)
    df['Buffer Stock'] = (df['Buffer Percentage'] / 100) * df['Mean Sale']

    # Step 8: Apply Capping to Buffer Stock Values
    lower_cap = df['Buffer Stock'].quantile(0.05)
    upper_cap = df['Buffer Stock'].quantile(0.95)
    df['Buffer Stock'] = df['Buffer Stock'].clip(lower=lower_cap, upper=upper_cap).round().astype(int)

    # Step 9: Handle Missing Values Using Forward and Backward Fill
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    df.fillna(df.groupby('Drug Name')['Sales'].transform('mean'), inplace=True)

    # Step 10: Arrange Columns in a Defined Order
    final_columns = ['Disease Category', 'Drug Category', 'Drug Name', 'Dosage', 'Retail Price',
                     'Purchase Price', 'Sales', 'Date', 'Year', 'Quarter', 'Month',
                     'Lag_1', 'Lag_2', 'Rolling_Mean_3', 'EMA_3', 'Mean Sale', 'CV',
                     'Buffer Percentage', 'Buffer Stock']
    df = df[final_columns]

    return df

# Main function to load data, apply feature engineering, and save the processed file
def main():
    input_file = "C:/C:/Users/ASUS/OneDrive/Desktop/Users/ASUS/OneDrive/Desktop/Final_combined_data.xlsx"
    output_file = "C:/Users/ASUS/OneDrive/Desktop/One_Drug_Data_Featured.xlsx"

    # Step 1: Load Data
    df = pd.read_excel(input_file)

    # Step 2: Apply Feature Engineering
    df = feature_engineering(df)

    # Step 3: Save Processed Data to Output File
    df.to_excel(output_file, index=False)
    print(f"Feature engineering completed and saved to {output_file}")

# Execute main function if script is run directly
if __name__ == "__main__":
    main()
