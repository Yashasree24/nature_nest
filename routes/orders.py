from flask import Blueprint, jsonify, request
from database import mongo

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/place', methods=['POST'])
def place_order():
    data = request.json
    order_id = mongo.db.orders.insert_one({
        "user_email": data["user_email"],
        "plant_id": data["plant_id"],
        "quantity": data["quantity"],
        "address": data["address"]
    }).inserted_id

    return jsonify({"message": "Order placed successfully", "order_id": str(order_id)})

@orders_bp.route('/history/<email>', methods=['GET'])
def order_history(email):
    orders = mongo.db.orders.find({"user_email": email})
    order_list = [{"id": str(o["_id"]), "plant_id": o["plant_id"], "quantity": o["quantity"]} for o in orders]
    return jsonify(order_list)
