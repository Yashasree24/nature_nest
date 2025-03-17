from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.plants import plants_bp
from routes.users import users_bp
from routes.orders import orders_bp
from routes.payments import payments_bp
from config.config import Config
from database.database import insert_sample_plants

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "supersecretkey"

CORS(app)
JWTManager(app)
insert_sample_plants()

app.register_blueprint(plants_bp, url_prefix='/api/plants')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(payments_bp, url_prefix='/api/payments')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Nature Nest API"})

if __name__ == '__main__':
    app.run(debug=True)
