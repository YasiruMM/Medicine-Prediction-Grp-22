import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Function to visualize outliers using box plots
def visualize_outliers(df, columns):
    """
    Generates a box plot to visualize outliers in the specified numeric columns.
    """
    print("Visualizing Outliers...")
    df[columns].boxplot(figsize=(10, 6))
    plt.title("Box Plot for Outlier Detection")
    plt.ylabel("Values")
    plt.show()


# Function to apply Winsorization (capping extreme values)
def apply_winsorization(df, columns, lower_percentile=0.05, upper_percentile=0.95):
    """
    Applies Winsorization by capping extreme values at the specified percentiles.
    """
    print("Applying Winsorization...")
    for col in columns:
        lower_bound = df[col].quantile(lower_percentile)
        upper_bound = df[col].quantile(upper_percentile)

        # Clip values to the defined bounds
        df[col] = np.clip(df[col], lower_bound, upper_bound)
        print(f"{col}: Winsorized to [{lower_bound}, {upper_bound}]")

    return df


# Function to clean invalid or unnecessary rows
def clean_invalid_rows(df, invalid_words=None):
    """
    Removes rows containing invalid values like 'unknown', 'n/a', 'null', etc.
    """
    if invalid_words is None:
        invalid_words = ["unknown", "n/a", "na", "null"]  # Define invalid words here

    print("Cleaning invalid rows...")
    # Replace all string values to lowercase for case-insensitive comparison
    invalid_regex = "|".join(invalid_words)
    df = df.replace(rf"(?i){invalid_regex}", np.nan, regex=True)  # Mark invalid cells as NaN

    # Drop rows with NaN in any column
    df = df.dropna()
    print("Rows with invalid values have been removed.")

    return df


# Function to process outliers and clean the dataset
def process_outliers(file_path, output_path):
    """
    Reads an Excel file, visualizes outliers, applies Winsorization, removes invalid rows,
    and saves the cleaned dataset.
    """
    # Load the dataset
    data = pd.read_excel(file_path)

    # Define numeric columns for outlier analysis
    numeric_columns = ['Retail Price', 'Purchase Price', 'Sales']

    # Visualize outliers in numeric columns
    visualize_outliers(data, numeric_columns)

    # Apply Winsorization to cap extreme values
    data = apply_winsorization(data, numeric_columns)

    # Remove invalid or unnecessary rows
    data = clean_invalid_rows(data)

    # Save the cleaned data to an Excel file
    data.to_excel(output_path, index=False)
    print(f"Winsorized data saved to {output_path}")


# File paths for input and output Excel files
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Processed.xlsx'
output_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Winsorized.xlsx'

# Execute the data cleaning and outlier processing function
process_outliers(input_file, output_file)
