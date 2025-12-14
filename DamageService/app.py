from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import get_all_damage_types, update_car_damages, get_car_damages_totals
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('KEY')
jwt = JWTManager(app)

@app.route('/damage-types', methods=['GET'])
def all_damage_types():
    damages = get_all_damage_types()
    return jsonify(damages)

@app.route('/car-damages', methods=['POST'])
def update_car_damage():
    data = request.json
    update_car_damages(data)
    return jsonify({"message": "Damages added"}), 201


@app.route('/car-damages', methods=['GET'])
def car_damages():
    totals = get_car_damages_totals()
    return jsonify(totals)

app.run(host='0.0.0.0', port=5003) 