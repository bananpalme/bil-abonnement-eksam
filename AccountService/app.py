from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import add_account, find_account_by_username
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('KEY')
jwt = JWTManager(app)

# register ny profil
@app.route('/profile', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if find_account_by_username(username):
        return jsonify({'message': 'Account already exists'}), 400
    
    add_account(username, password, role)

    return jsonify({'message': f'Account registered successfully'}), 201

@app.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    current_user = get_jwt_identity()

    user = find_account_by_username(current_user)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'username': user['username'], 'id': user['id']}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    account = find_account_by_username(username)

    if not account or account['password'] != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    role = account['role']

    # Create JWT token
    token = create_access_token(identity=username, additional_claims={"role": role})

    response = make_response(jsonify({
        'message': 'Login successful',
        'username': username,
        'role': role
    }), 200)
    response.headers['Authorization'] = f'Bearer {token}'
    return response

app.run(host='0.0.0.0', port=5003)