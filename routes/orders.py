from flask import Blueprint, jsonify, request
from database.database import orders_collection, plants_collection
from bson.objectid import ObjectId

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/place', methods=['POST'])
def place_order():
    data = request.json
    plant = plants_collection.find_one({"_id": ObjectId(data["plant_id"])})

    if not plant or plant["stock"] < data["quantity"]:
        return jsonify({"error": "Not enough stock available"}), 400

    plants_collection.update_one({"_id": plant["_id"]}, {"$inc": {"stock": -data["quantity"]}})
    
    order_id = orders_collection.insert_one({
        "user_email": data["user_email"],
        "plant_id": data["plant_id"],
        "quantity": data["quantity"],
        "address": data["address"]
    }).inserted_id

    return jsonify({"message": "Order placed successfully!", "order_id": str(order_id)})

@orders_bp.route('/history/<email>', methods=['GET'])
def order_history(email):
    orders = orders_collection.find({"user_email": email})
    return jsonify([{"id": str(o["_id"]), "plant_id": o["plant_id"], "quantity": o["quantity"]} for o in orders])
