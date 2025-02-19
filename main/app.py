from flask import Flask, jsonify
from flask_cors import CORS
from routes.plants import plants_bp
from routes.users import users_bp
from routes.orders import orders_bp
from main.config import Config
from main.database import mongo

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # Enable CORS
mongo.init_app(app)  # Initialize MongoDB

# Register blueprints (modular routes)
app.register_blueprint(plants_bp, url_prefix='/api/plants')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Nature Nest API"})

if __name__ == '__main__':
    app.run(debug=True)
