from flask import Blueprint, request, jsonify, session
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

auth_controller = Blueprint('auth', __name__)

users_collection = db["users"]

@auth_controller.route("/login", methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = users_collection.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid username or password"}), 401

    session['user_id'] = str(user["_id"])
    user["_id"] = str(user["_id"])
    return jsonify(user), 200

@auth_controller.route("/register", methods=['POST'])
def register():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    # Check if the username is already taken
    existing_user = users_collection.find_one({"username": email})
    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')

    new_user = {"first_name": first_name, "last_name":last_name,"email": email, "password": hashed_password}
    users_collection.insert_one(new_user)
    new_user["_id"] = str(new_user["_id"])
    return jsonify(new_user), 201

@auth_controller.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200
