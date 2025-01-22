import pandas as pd
import matplotlib.pyplot as plt

# Function to visualize outliers using box plots
def visualize_outliers(df, columns):
    print("Visualizing Outliers...")
    df[columns].boxplot(figsize=(10, 6))
    plt.title("Box Plot for Outlier Detection")
    plt.ylabel("Values")
    plt.show()

# Function to remove outliers using the 1.5×IQR rule
def remove_outliers(df, columns):
    print("Removing Outliers...")
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filter out rows with values outside the acceptable range
        initial_rows = df.shape[0]
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        final_rows = df.shape[0]

        print(f"{col}: Removed {initial_rows - final_rows} outliers.")

    return df

# Example Usage: Detecting and Removing Outliers
def process_outliers(file_path, output_path):
    # Load the dataset
    data = pd.read_excel(file_path)

    # Visualize outliers in numeric columns
    numeric_columns = ['Retail Price', 'Purchase Price', 'Sales']
    visualize_outliers(data, numeric_columns)

    # Remove outliers from numeric columns
    cleaned_data = remove_outliers(data, numeric_columns)

    # Save the cleaned data
    cleaned_data.to_excel(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

# File paths
input_file1 = 'C:/Users/ASUS/OneDrive/Desktop/Atorvastatin_Cleaned_Processed.xlsx'
output_file1 = 'C:/Users/ASUS/OneDrive/Desktop/Atorvastatin_NoOutliers.xlsx'

input_file2 = 'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin_Cleaned_Processed.xlsx'
output_file2 = 'C:/Users/ASUS/OneDrive/Desktop/Rosuvastatin_NoOutliers.xlsx'

input_file3 = 'C:/Users/ASUS/OneDrive/Desktop/Simvastatin_Cleaned_Processed.xlsx'
output_file3 = 'C:/Users/ASUS/OneDrive/Desktop/Simvastatin_NoOutliers.xlsx'

process_outliers(input_file1, output_file1)
process_outliers(input_file2,output_file2)
process_outliers(input_file3, output_file3)




