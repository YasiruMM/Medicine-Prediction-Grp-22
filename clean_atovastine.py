import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Folder containing Atovastine files
folder_path = "path_to_Atovastine_folder"
output_file = "cleaned_atovastine.xlsx"


# 1. Load all Excel files
def load_data(folder_path):
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    dataframes = [pd.read_excel(file) for file in all_files]
    combined_data = pd.concat(dataframes, ignore_index=True)
    return combined_data


# 2. Perform EDA
def perform_eda(data):
    print("\nBasic Info:")
    print(data.info())

    print("\nSummary Statistics:")
    print(data.describe())

    print("\nMissing Values:")
    print(data.isnull().sum())

    print("\nDuplicate Rows:")
    print(data.duplicated().sum())

    # Visualization Examples
    sns.histplot(data['Margin'], kde=True)
    plt.title('Distribution of Margins')
    plt.show()

    sns.scatterplot(x='GP', y='Margin', data=data)
    plt.title('GP vs Margin')
    plt.show()


# 3. Clean the Data
def clean_data(data):
    # Drop duplicates
    data = data.drop_duplicates()

    # Handle missing values (example: fill with 0 or mean)
    data = data.fillna(0)  # Adjust based on your needs

    # Example: Remove outliers in 'Margin'
    q1 = data['Margin'].quantile(0.25)
    q3 = data['Margin'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    data = data[(data['Margin'] >= lower_bound) & (data['Margin'] <= upper_bound)]

    return data


# 4. Save cleaned data
def save_cleaned_data(data, output_file):
    data.to_excel(output_file, index=False)


# Main Execution
if __name__ == "__main__":
    # Load the data
    raw_data = load_data(folder_path)

    # Perform EDA
    perform_eda(raw_data)

    # Clean the data
    cleaned_data = clean_data(raw_data)

    # Save the cleaned data
    save_cleaned_data(cleaned_data, output_file)
    print(f"Cleaned data saved to {output_file}")
