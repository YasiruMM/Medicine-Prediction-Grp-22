import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Load the dataset
data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured.xlsx')

# Identify categorical features
categorical_features = data.select_dtypes(include=['object', 'category']).columns
print("Categorical features:", categorical_features)

# Apply One-Hot Encoding
encoder = OneHotEncoder(sparse_output=False, drop='first')  # drop='first' to avoid multicollinearity
encoded_features = encoder.fit_transform(data[categorical_features])

# Convert encoded features to a DataFrame with meaningful column names
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))

# Drop original categorical columns and concatenate encoded features
data = data.drop(categorical_features, axis=1)
data = pd.concat([data, encoded_df], axis=1)

# Save the encoded dataset
data.to_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured_Encoded.xlsx', index=False)

print("Encoded dataset saved successfully!")

from sklearn.model_selection import train_test_split

# Load the encoded dataset
encoded_data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured_Encoded.xlsx')

# Define features (X) and target (y)
features = encoded_data.drop(columns=['Sales'])  # Drop the target column
target = encoded_data['Sales']  # Target column

# Split the dataset into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Check the sizes of the train and test sets
print(f"Train data size: {len(X_train)}")
print(f"Test data size: {len(X_test)}")