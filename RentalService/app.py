from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import get_all_clients
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
    
@app.route('/client', methods=['GET'])
def client_overview():
    clients = get_all_clients()

    return jsonify(clients)

@app.route('/cars', methods=['GET'])
def show_cars():
    return jsonify({"message": "I LOVE CARS SO MUCH YIPEE!!"})

app.run(host='0.0.0.0', port=5001)