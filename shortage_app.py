from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from flask_cors import CORS
import os

# Get the absolute path of the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Initialize Flask App
shortage_app = Flask(__name__)
CORS(shortage_app, resources={r"/*": {"origins": "*"}})

# File paths for datasets and model (relative to the project root)
model_path = os.path.join(PROJECT_ROOT, "model", "RandomForest_OOS.pkl")
features_file = os.path.join(PROJECT_ROOT, "data", "NoiseHandled1_MediTrack_Dataset.csv")
predictions_file = os.path.join(PROJECT_ROOT, "data", "XGBoost_Predictions.csv")

# Load the trained Random Forest model
try:
    rf_model = joblib.load(model_path)
    print("Random Forest Model Loaded Successfully!")
except Exception as e:
    print(f"Error Loading Model: {e}")

# Generate the merged dataset
def generate_merged_dataset():
    try:
        # Load datasets
        df_features = pd.read_csv(features_file)
        df_predictions = pd.read_csv(predictions_file)

        # Transform XGBoost Predictions to Log Scale
        prediction_cols = ["Prediction 1", "Prediction 2", "Prediction 3",
                           "Prediction 4", "Prediction 5", "Prediction 6"]
        df_predictions[prediction_cols] = np.log1p(df_predictions[prediction_cols])

        # Keep Only Forecasted Drugs
        df_filtered = df_features[df_features["Drug Name"].isin(df_predictions["Drug Name"])]

        # Aggregate numeric features
        agg_dict = {
            "Retail Price": "mean",
            "Purchase Price": "mean",
            "Sales": "sum",
            "Mean Sales": "mean",
            "Buffer Stock": "mean",
            "Sales_LOESS_Date": "first"
        }
        df_features_agg = df_filtered.groupby("Drug Name", as_index=False).agg(agg_dict)

        # Merge aggregated features with predictions
        df_merged = df_features_agg.merge(df_predictions, on="Drug Name", how="left")

        df_merged.drop(columns=["Disease Category_y"], inplace=True, errors="ignore")
        df_merged.rename(columns={"Disease Category_x": "Disease Category"}, inplace=True)

        df_merged = df_merged.drop_duplicates(
            subset=["Drug Name", "Prediction 1", "Prediction 2",
                    "Prediction 3", "Prediction 4", "Prediction 5", "Prediction 6"],
            keep="first"
        )

        df_merged["Log_Sales"] = np.log1p(df_merged["Sales"])
        df_merged["Log_Retail_Price"] = np.log1p(df_merged["Retail Price"])
        df_merged["Log_Purchase_Price"] = np.log1p(df_merged["Purchase Price"])
        df_merged["Log_Buffer_Stock"] = np.log1p(df_merged["Buffer Stock"])

        # Assign risk factors based on Disease Category
        loss_factors = {'Cardiovascular': 0.20, 'Diabetes': 0.25, 'Cholesterol': 0.15}
        df_merged['Loss Factor'] = df_merged['Disease Category'].map(loss_factors).fillna(0.15)
        df_merged['Loss Quantity'] = df_merged['Loss Factor'] * df_merged["Log_Sales"]
        df_merged['Loss Quantity'] = df_merged['Loss Quantity'].apply(lambda x: max(0, x))

        df_merged.drop(columns=['Date', 'Month', 'Year'], inplace=True, errors="ignore")

        df_merged["Original Drug Name"] = df_merged["Drug Name"]

        df_merged = pd.get_dummies(df_merged, columns=['Disease Category', 'Drug Name'], drop_first=True)

        return df_merged

    except Exception as e:
        print(f"Error Generating Dataset: {e}")
        return None

@shortage_app.route('/get-drug-names', methods=['GET'])
def get_drug_names():
    try:
        category = request.args.get("category")
        df_features = pd.read_csv(features_file)

        if category:
            category_cleaned = category.strip().lower()
            df_filtered = df_features[df_features["Disease Category"].str.lower() == category_cleaned]
        else:
            df_filtered = df_features

        available_drugs = df_filtered["Drug Name"].unique().tolist()
        return jsonify({"drug_names": available_drugs})

    except Exception as e:
        return jsonify({"error": str(e)})

@shortage_app.route('/predict-oos', methods=['POST'])
def predict_oos():
    try:
        user_input = request.get_json()
        user_drug = user_input.get("drug_name")
        user_loss = user_input.get("loss_quantity")

        df_merged = generate_merged_dataset()
        if df_merged is None:
            return jsonify({"error": "Failed to generate dataset!"})

        if user_drug not in df_merged["Original Drug Name"].values:
            return jsonify({"error": f"Drug '{user_drug}' not found!"})

        buffer_stock = df_merged[df_merged["Original Drug Name"] == user_drug]["Buffer Stock"].values[0]
        max_loss_threshold = buffer_stock * 1.5
        user_loss = min(user_loss, max_loss_threshold)

        X_user = df_merged[df_merged["Original Drug Name"] == user_drug].copy()
        X_user["Loss Quantity"] = np.log1p(user_loss)

        features = ['Sales_LOESS_Date', 'Log_Sales', 'Log_Buffer_Stock', 'Log_Retail_Price',
                    'Log_Purchase_Price', 'Loss Quantity'] + list(
            df_merged.columns[df_merged.columns.str.startswith(('Disease Category_', 'Drug Name_'))])

        X_user = X_user[features]
        y_pred_log = rf_model.predict(X_user)
        y_pred_exp = np.expm1(y_pred_log).flatten()

        # Get original predictions from XGBoost predictions
        xgb_original = df_merged[df_merged["Original Drug Name"] == user_drug][
            ["Prediction 1", "Prediction 2", "Prediction 3", "Prediction 4", "Prediction 5",
             "Prediction 6"]].values.flatten()
        xgb_original_exp = np.expm1(xgb_original)  # Exponentiate to get actual prediction values

        # Calculate shortage risk
        shortage_risk = np.array(xgb_original_exp) - np.array(y_pred_exp)
        shortage_risk_levels = [val if val > 0 else 0 for val in shortage_risk]

        result = {
            "drug_name": user_drug,
            "loss_quantity": user_loss,
            "buffer_stock": buffer_stock,
            "original_predictions": xgb_original_exp.tolist(),
            "adjusted_predictions": y_pred_exp.tolist(),
            "shortage_risk_levels": shortage_risk_levels
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

@shortage_app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "Shortage App is running!"})

if __name__ == "__main__":
    from waitress import serve
    print("Starting shortage app with Waitress on port 5002...")
    serve(shortage_app, host="127.0.0.1", port=5002)
