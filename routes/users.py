from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from database import mongo
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

# User Registration (Already Exists)
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(data["password"])
    
    mongo.db.users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password,
        "address": data.get("address", "")
    })
    return jsonify({"message": "User registered successfully"})

# User Login (Modified to use password hashing)
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})
    
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])
    return jsonify({"token": token, "message": "Login successful"})

# Get User Profile
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({"email": current_user}, {"password": 0})  # Exclude password
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Update User Profile
@users_bp.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.json

    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "address" in data:
        update_data["address"] = data["address"]
    if "password" in data:
        update_data["password"] = generate_password_hash(data["password"])  # Hash new password

    mongo.db.users.update_one({"email": current_user}, {"$set": update_data})
    return jsonify({"message": "Profile updated successfully"})

# Fetch User's Order History
@users_bp.route('/orders', methods=['GET'])
@jwt_required()
def user_orders():
    current_user = get_jwt_identity()
    orders = list(mongo.db.orders.find({"user_email": current_user}))

    for order in orders:
        order["_id"] = str(order["_id"])
        plant = mongo.db.plants.find_one({"_id": ObjectId(order["plant_id"])})
        order["plant_name"] = plant["name"] if plant else "Unknown Plant"

    return jsonify(orders)
