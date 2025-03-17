from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import mongo
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])  # Hash password
    mongo.db.users.insert_one({"name": data["name"], "email": data["email"], "password": hashed_password})
    
    return jsonify({"message": "User registered successfully"})

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])
    return jsonify({"token": token, "message": "Login successful"})

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user}, {"password": 0})  # Exclude password from response
    return jsonify(user)
