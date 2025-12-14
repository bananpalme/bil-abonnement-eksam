from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import get_all_clients, get_cars, get_client_by_id, make_new_contract, get_all_contracts
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('KEY')
jwt = JWTManager(app)
    
# show all clients
@app.route('/client', methods=['GET'])
@jwt_required()
def client_overview():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")
    
    if role not in [ "dataregistry", "admin"]:
        return jsonify({"message": "Unnauthorized"}), 403

    clients = get_all_clients()

    return jsonify(clients)

@app.route('/cars', methods=['GET'])
@jwt_required()
def show_cars():
    claims = get_jwt()
    role = claims.get("role")
    if role not in ["dataregistry", "admin", "damages"]:
        return jsonify({"message": "Unauthorized"}), 403
    cars = get_cars()

    return jsonify(cars)

@app.route('/contract', methods=['POST'])
@jwt_required()
def new_contract():
    claims = get_jwt()
    role = claims.get("role")
    
    if role not in [ "dataregistry", "admin"]:
        return jsonify({"message": "Unnauthorized"}), 403

    data = request.json
    client_id = data.get("client_id")
    car_id = data.get("car_id")
    months = data.get("months")
    monthly_rate = data.get("monthly_rate")
    total_cost = months * monthly_rate

    make_new_contract(client_id, car_id, months, monthly_rate, total_cost)

    return jsonify({"message": "Rental contract created"}), 201

@app.route('/contract', methods=['GET'])
@jwt_required()
def all_contracts():
    claims = get_jwt()
    role = claims.get("role")
    if role not in ["dataregistry", "admin"]:
        return jsonify({"message": "Unauthorized"}), 403
    
    try:
        contracts = get_all_contracts()
        return jsonify(contracts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host='0.0.0.0', port=5001) 