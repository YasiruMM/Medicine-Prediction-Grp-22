import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load the encoded dataset
encoded_data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured_Encoded.xlsx')

# Define features (X) and target (y)
X = encoded_data.drop(columns=['Sales'])  # Drop the target column
y = encoded_data['Sales']  # Target column

# Convert continuous 'Sales' to discrete categories
# Define bins and labels for classification
bins = [0, 100, 200, float('inf')]  # Adjust ranges based on your dataset
labels = ['Low', 'Medium', 'High']
y = pd.cut(y, bins=bins, labels=labels)
# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
rf_predictions = rf_model.predict(X_test)

# Evaluation
print("Random Forest Accuracy:", accuracy_score(y_test, rf_predictions))
print(classification_report(y_test, rf_predictions))
