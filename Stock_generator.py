import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'
output_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_With_Stock.xlsx'

try:
    # Read the Excel file
    data = pd.read_excel(input_file)

    # Ensure required columns are present
    if 'Sales' not in data.columns:
        raise ValueError("The 'Sales' column is required to calculate 'Mean Sale'.")

    if 'Date' in data.columns:
        data = data.sort_values(by=['Drug Name', 'Date'], ascending=[True, True])
    else:
        data = data.sort_values(by=['Drug Name'])

    # Step 1: Generate 'Mean Sale'
    # Group by relevant columns (e.g., Drug, Dosage) if applicable and calculate mean
    data['Mean Sale'] = data.groupby(['Drug', 'Dosage'])['Sales'].transform('mean')

    # Step 2: Calculate Coefficient of Variation (CV)
    data['CV'] = data.groupby(['Drug', 'Dosage'])['Sales'].transform(lambda x: (x.std() / x.mean()) * 100)


    # Step 3: Define 'Buffer Percentage' based on CV
    def buffer_percentage(cv):
        if cv <= 20:
            return 20
        elif 20 < cv <= 50:
            return 30
        else:
            return 50


    data['Buffer Percentage'] = data['CV'].apply(buffer_percentage)

    # Step 4: Calculate 'Buffer Stock'
    data['Buffer Stock'] = data['Buffer Percentage'] / 100 * data['Mean Sale']
    # Step 5: Apply capping to 'Buffer Stock'
    buffer_stock_lower_cap = data['Buffer Stock'].quantile(0.05)  # 5th percentile
    buffer_stock_upper_cap = data['Buffer Stock'].quantile(0.95)  # 95th percentile
    data['Buffer Stock'] = data['Buffer Stock'].clip(lower=buffer_stock_lower_cap, upper=buffer_stock_upper_cap)

    # Step 6: Round 'Buffer Stock' to nearest integer
    data['Buffer Stock'] = data['Buffer Stock'].round().astype(int)

    # Step 7: Visualize 'Buffer Stock' after capping
    plt.figure(figsize=(10, 5))
    plt.boxplot(data['Buffer Stock'])
    plt.title('Buffer Stock - After Capping and Rounding')
    plt.show()

    # Save the updated dataset to an Excel file
    data.to_excel(output_file, index=False)

    print(f"Generated columns and saved updated file to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
