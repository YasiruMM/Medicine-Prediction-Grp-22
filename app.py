# filepath: /C:/Users/user/Documents/GitHub/Medicine-Prediction-Grp-22/app.py
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Medicine_Accuracy_DB']

@app.route('/')
def index():
    # Fetch data from MongoDB collection
    collection = db['Cardiovascular']  # Ensure this is the correct collection name
    data = list(collection.find())
    return render_template('index.html', data=data)

@app.route('/cholesterol')
def cholesterol():
    # Fetch data from MongoDB collection
    collection = db['Cholesterol']
    data = list(collection.find())
    return render_template('cholesterol.html', data=data)

@app.route('/diabetes')
def diabetes():
    # Fetch data from MongoDB collection
    collection = db['Diabetes']
    data = list(collection.find())
    return render_template('diabetes.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)