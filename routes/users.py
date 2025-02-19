from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from database import mongo

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400
    
    mongo.db.users.insert_one({"name": data["name"], "email": data["email"], "password": data["password"]})
    return jsonify({"message": "User registered successfully"})

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"], "password": data["password"]})
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])
    return jsonify({"token": token, "message": "Login successful"})
