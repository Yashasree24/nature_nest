from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from database import mongo

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/place', methods=['POST'])
@jwt_required()
def place_order():
    data = request.json
    current_user = get_jwt_identity()  # Get logged-in user's email

    # Fetch the plant from the database
    plant = mongo.db.plants.find_one({"_id": ObjectId(data["plant_id"])})
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    # Check if enough stock is available
    if plant["stock"] < data["quantity"]:
        return jsonify({"error": "Not enough stock available"}), 400

    # Insert order
    order_id = mongo.db.orders.insert_one({
        "user_email": current_user,
        "plant_id": data["plant_id"],
        "quantity": data["quantity"],
        "address": data["address"],
        "status": "Pending"
    }).inserted_id

    # Reduce stock count
    mongo.db.plants.update_one({"_id": ObjectId(data["plant_id"])}, {"$inc": {"stock": -data["quantity"]}})

    return jsonify({"message": "Order placed successfully!", "order_id": str(order_id)})

@orders_bp.route('/history', methods=['GET'])
@jwt_required()
def order_history():
    current_user = get_jwt_identity()
    orders = mongo.db.orders.find({"user_email": current_user})
    order_list = [{
        "id": str(o["_id"]),
        "plant_id": o["plant_id"],
        "quantity": o["quantity"],
        "status": o["status"]
    } for o in orders]
    return jsonify(order_list)
