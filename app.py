from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MedicineDB"]
collection = db["Medicines"]

@app.route("/")
def index():
    data = list(collection.find({}, {"_id": 0}))  # Fetch data, excluding _id
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
