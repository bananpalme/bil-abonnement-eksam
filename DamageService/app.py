from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import get_all_damage_types, update_car_damages, get_car_damages_totals
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('KEY')
jwt = JWTManager(app)

@app.route('/damage-types', methods=['GET'])
def all_damage_types():
    damages = get_all_damage_types()
    return jsonify(damages)

@app.route('/car-damages', methods=['POST'])
@jwt_required()
def update_car_damage():
    claims = get_jwt()
    role = claims.get("role")
    if role not in ["damages", "admin"]:
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.json
    update_car_damages(data)
    return jsonify({"message": "Damages added"}), 201


@app.route('/car-damages', methods=['GET'])
@jwt_required()
def car_damages():
    claims = get_jwt()
    role = claims.get("role")
    if role not in ["damages", "admin"]:
        return jsonify({"message": "Unauthorized"}), 403

    totals = get_car_damages_totals()
    return jsonify(totals)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port)