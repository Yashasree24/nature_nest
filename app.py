from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.plants import plants_bp
from routes.users import users_bp
from routes.orders import orders_bp
from config import Config
from database import mongo

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # Enable CORS
mongo.init_app(app)  # Initialize MongoDB

app.config["JWT_SECRET_KEY"] = "your_secret_key_here"  # Change this to a secure secret key
jwt = JWTManager(app)  # Initialize JWT

# Register blueprints
app.register_blueprint(plants_bp, url_prefix='/api/plants')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Nature Nest API"})

if __name__ == '__main__':
    app.run(debug=True)
