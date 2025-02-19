from flask import Blueprint, jsonify, request
from database import mongo

plants_bp = Blueprint('plants', __name__)

@plants_bp.route('/', methods=['GET'])
def get_plants():
    plants = mongo.db.plants.find()
    plant_list = [{"id": str(p["_id"]), "name": p["name"], "category": p["category"], "price": p["price"]} for p in plants]
    return jsonify(plant_list)

@plants_bp.route('/add', methods=['POST'])
def add_plant():
    data = request.json
    mongo.db.plants.insert_one({
        "name": data["name"],
        "category": data["category"],
        "price": data["price"]
    })
    return jsonify({"message": "Plant added successfully!"})
