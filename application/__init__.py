from flask_pymongo import PyMongo
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SECRET_KEY"] = "f0737effe28285dd6f9e50f17b9e41d86f86afbe"
app.config["MONGO_URI"] = "mongodb+srv://ecoprints:456abc@cluster0.inyuslv.mongodb.net/ecoprints?retryWrites=true&w=majority"

# mongodb database
mongodb = PyMongo(app)
db = mongodb.db

@app.route('/check_connection', methods=['GET'])
def check_connection():
    if mongodb.cx.is_primary:
        return "Connected to MongoDB"
    else:
        return "Failed to connect to MongoDB"