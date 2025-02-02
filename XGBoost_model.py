import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load the encoded dataset
encoded_data = pd.read_excel('C:/Users/ASUS/OneDrive/Desktop/Drug_Data_Featured_Encoded.xlsx')

# Define features (X) and target (y)
X = encoded_data.drop(columns=['Sales'])  # Drop the target column
y = encoded_data['Sales']  # Target column

# Convert continuous 'Sales' to discrete categories
bins = [0, 100, 200, float('inf')]  # Adjust ranges based on your dataset
labels = [0, 1, 2]  # Encoding categories as 0 (Low), 1 (Medium), 2 (High)
y = pd.cut(y, bins=bins, labels=labels).astype(int)  # Convert to numerical labels

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost Model
xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
xgb_model.fit(X_train, y_train)

# Predictions
xgb_predictions = xgb_model.predict(X_test)

# Evaluation
print("XGBoost Accuracy:", accuracy_score(y_test, xgb_predictions))
print(classification_report(y_test, xgb_predictions))
