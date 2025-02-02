import matplotlib.pyplot as plt
import pandas as pd

# Load your dataset
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'
data = pd.read_excel(input_file)

# Check if the 'Date' column exists
if 'Date' not in data.columns:
    raise ValueError("The 'Date' column is missing in the dataset.")

# Handle invalid or missing dates
def process_date(x):
    try:
        if isinstance(x, (int, float)):
            x = str(x)
        # Handle 'MM.YY' format
        if isinstance(x, str) and '.' in x:
            month, year_suffix = x.split('.')
            year = f"20{year_suffix.strip()}"
            month = int(month.strip())
            return f"{year}-{month:02d}-01"
        # Handle valid full dates (e.g., '2024-02-01')
        elif pd.to_datetime(x, errors='coerce') is not pd.NaT:
            return x
    except Exception as e:
        print(f"Error processing date: {x} - {e}")
    return None


# Apply the date processing function
data['Processed_Date'] = data['Date'].apply(process_date)

print("Processed_Date Column:\n", data['Processed_Date'].head())
print("Converted Date Column:\n", data['Date'].head())

# Convert the processed dates to datetime
data['Date'] = pd.to_datetime(data['Processed_Date'], errors='coerce')

# Drop rows with invalid dates
data = data.dropna(subset=['Date'])

# Check the date range of the dataset
print(f"Dataset date range: {data['Date'].min()} to {data['Date'].max()}")

# Split the data into training and testing sets
train_data = data[data['Date'] < '2024-05-01']
test_data = data[data['Date'] >= '2024-05-01']

# Save the train and test sets if needed
train_data.to_excel('train_data.xlsx', index=False)
test_data.to_excel('test_data.xlsx', index=False)

print("Train and test datasets created successfully!")

print(f"Training set size: {len(train_data)}")
print(f"Testing set size: {len(test_data)}")

