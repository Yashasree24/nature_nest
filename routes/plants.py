from flask import Blueprint, jsonify, request
from database import mongo

plants_bp = Blueprint('plants', __name__)

# Get all plants
@plants_bp.route('/', methods=['GET'])
def get_plants():
    plants = mongo.db.plants.find()
    plant_list = [
        {
            "id": str(p["_id"]),
            "name": p["name"],
            "category": p["category"],
            "price": p["price"],
            "image_url": p["image_url"],
            "stock": p["stock"],
            "description": p["description"]
        }
        for p in plants
    ]
    return jsonify(plant_list)

# Add a new plant
@plants_bp.route('/add', methods=['POST'])
def add_plant():
    data = request.json

    # Validate required fields
    if not all(key in data for key in ["name", "category", "price", "image_url", "stock", "description"]):
        return jsonify({"error": "Missing fields"}), 400

    plant_id = mongo.db.plants.insert_one({
        "name": data["name"],
        "category": data["category"],
        "price": data["price"],
        "image_url": data["image_url"],
        "stock": data["stock"],
        "description": data["description"]
    }).inserted_id

    return jsonify({"message": "Plant added successfully", "plant_id": str(plant_id)})

# Get a single plant by ID
@plants_bp.route('/<plant_id>', methods=['GET'])
def get_plant(plant_id):
    plant = mongo.db.plants.find_one({"_id": mongo.ObjectId(plant_id)})

    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    plant_data = {
        "id": str(plant["_id"]),
        "name": plant["name"],
        "category": plant["category"],
        "price": plant["price"],
        "image_url": plant["image_url"],
        "stock": plant["stock"],
        "description": plant["description"]
    }
    return jsonify(plant_data)
