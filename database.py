from config import db

# Reference to the plants collection
plants_collection = db["plants"]

# Function to insert sample plants into MongoDB
def insert_sample_plants():
    sample_plants = [
        {
            "name": "Aloe Vera",
            "type": "Medicinal",
            "sunlight": "Partial",
            "water": "Low",
            "soil": "Sandy",
            "size": "Small",
            "price": 5,
            "image_url": "/images/aloe.jpg",
            "stock": 20,
            "description": "Good for skin care."
        },
        {
            "name": "Rose",
            "type": "Flowering",
            "sunlight": "Full",
            "water": "Moderate",
            "soil": "Loamy",
            "size": "Medium",
            "price": 10,
            "image_url": "/images/rose.jpg",
            "stock": 15,
            "description": "Beautiful and fragrant."
        }
    ]
    
    # Insert data only if the collection is empty
    if plants_collection.count_documents({}) == 0:
        plants_collection.insert_many(sample_plants)
        print("Sample plants inserted.")
    else:
        print("Plants already exist in the database.")

# Function to retrieve all plants
def get_all_plants():
    return list(plants_collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id field
