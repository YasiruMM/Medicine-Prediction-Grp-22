import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

#  Create or use an existing database
db = client['Medicine_Accuracy_DB']  # Replace  with  desired database name

# Function to import a CSV file into a MongoDB collection
def import_csv_to_mongodb(csv_file, collection_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Convert the DataFrame to a list of dictionaries (one dictionary per row)
    data = df.to_dict(orient='records')
    
    # Insert the data into the specified collection
    db[collection_name].insert_many(data)
    print(f"Imported {len(data)} documents into the '{collection_name}' collection.")

# Step 4: Import each CSV file into its respective collection
import_csv_to_mongodb('Cardiovascular.csv', 'Cardiovascular')      
import_csv_to_mongodb('Cholesterol.csv', 'Cholesterol') 
import_csv_to_mongodb('Diabetes.csv', 'Diabetes')    

print("All data imported successfully!")