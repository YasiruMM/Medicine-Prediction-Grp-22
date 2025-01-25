import matplotlib.pyplot as plt
import pandas as pd


data=pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx')
data['Sales'].hist(bins=50)
plt.title('Sales Distribution')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.show()

import pandas as pd

# Load your dataset
input_file = 'C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx'
data = pd.read_excel(input_file)

# Ensure 'Date' column is in datetime format
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Convert to datetime, handle errors
    if data['Date'].isna().any():
        print("Warning: Some rows have invalid or missing dates and will be dropped.")
        data = data.dropna(subset=['Date'])  # Drop rows with invalid/missing dates
else:
    raise ValueError("The 'Date' column is missing in the dataset.")

# Split the data into training and testing sets
train_data = data[data['Date'] < '2023-01-01']
test_data = data[data['Date'] >= '2023-01-01']

# Save the train and test sets if needed
train_data.to_excel('train_data.xlsx', index=False)
test_data.to_excel('test_data.xlsx', index=False)

print("Train and test datasets created successfully!")
