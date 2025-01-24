import pandas as pd

# Load your dataset
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'
output_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_With_Stock.xlsx'

try:
    # Read the Excel file
    data = pd.read_excel(input_file)

    # Ensure required columns are present
    if 'Sales' not in data.columns:
        raise ValueError("The 'Sales' column is required to calculate 'Mean Sale'.")

    # Step 1: Generate 'Mean Sale'
    # Group by relevant columns (e.g., Drug, Dosage) if applicable and calculate mean
    data['Mean Sale'] = data.groupby(['Drug', 'Dosage'])['Sales'].transform('mean')

    # Step 2: Add default 'Buffer Perc' column
    data['Buffer Perc'] = 20  # Default value of 20%

    # Step 3: Calculate 'Buffer Stock'
    data['Buffer Stock'] = data['Mean Sale'] * (data['Buffer Perc'] / 100)

    # Save the updated dataset to an Excel file
    data.to_excel(output_file, index=False)

    print(f"Generated columns and saved updated file to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
