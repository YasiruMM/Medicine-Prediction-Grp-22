import pandas as pd
import numpy as np
import re
from scipy.stats.mstats import winsorize


def standardize_drug_name(drug_name):
    """Removes dosage information and standardizes drug names."""
    if not isinstance(drug_name, str):
        return 'Unknown'
    return re.sub(r'\s*\d+\s*MG', '', drug_name, flags=re.IGNORECASE).strip()

def feature_engineering(df):
    """Applies feature engineering for drug demand forecasting."""

    # Step 1: Standardize Drug Names
    df['Standardized Drug Name'] = df['Drug Name'].apply(standardize_drug_name)
    df['Drug Identifier'] = df['Standardized Drug Name'] + ' ' + df['Dosage'].astype(str)
    df['Drug Name'] = df['Drug Identifier']
    df.drop(columns=['Standardized Drug Name', 'Drug Identifier'], inplace=True)

    # Step 2: Date Handling
    df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%m.%y', errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter

    # Step 3: Lag-Based Features
    for lag in range(1, 3):  # Lag_1, Lag_2
        df[f'Lag_{lag}'] = df.groupby('Drug Name')['Sales'].shift(lag)


    # Step 4: Rolling & EMA Features
    df['Rolling_Mean_3'] = df.groupby('Drug Name')['Sales'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df['EMA_3'] = df.groupby('Drug Name')['Sales'].transform(lambda x: x.ewm(span=3, adjust=False).mean())

    # Step 5: Mean Sales Calculation
    df['Mean Sale'] = df.groupby(['Drug Name'])['Sales'].transform('mean')

    # Step 6: Coefficient of Variation (CV)
    df['CV'] = df.groupby(['Drug Name'])['Sales'].transform(lambda x: (x.std() / x.mean()) * 100)

    # Step 7: Buffer Stock Calculation
    def buffer_percentage(cv):
        if cv <= 20:
            return 20
        elif 20 < cv <= 50:
            return 30
        else:
            return 50

    df['Buffer Percentage'] = df['CV'].apply(buffer_percentage)
    df['Buffer Stock'] = (df['Buffer Percentage'] / 100) * df['Mean Sale']

    # Apply capping to Buffer Stock
    lower_cap = df['Buffer Stock'].quantile(0.05)
    upper_cap = df['Buffer Stock'].quantile(0.95)
    df['Buffer Stock'] = df['Buffer Stock'].clip(lower=lower_cap, upper=upper_cap).round().astype(int)

    # Step 9: Fill Missing Values
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    df.fillna(df.groupby('Drug Name')['Sales'].transform('mean'), inplace=True)

    # Step 10: Ensure Columns Order
    final_columns = ['Disease Category', 'Drug Category', 'Drug Name', 'Dosage', 'Retail Price','Purchase Price', 'Sales', 'Date', 'Year', 'Quarter', 'Month','Lag_1', 'Lag_2', 'Rolling_Mean_3', 'EMA_3', 'Mean Sale', 'CV','Buffer Percentage', 'Buffer Stock',]
    df = df[final_columns]

    return df


def main():
    input_file = "C:/Users/ASUS/OneDrive/Desktop/Final_combined_data.xlsx"
    output_file = "C:/Users/ASUS/OneDrive/Desktop/One_Drug_Data_Featured.xlsx"

    # Load Data
    df = pd.read_excel(input_file)

    # Feature Engineering
    df = feature_engineering(df)

    # Save Processed Data
    df.to_excel(output_file, index=False)
    print(f"Feature engineering completed and saved to {output_file}")


if __name__ == "__main__":
    main()
