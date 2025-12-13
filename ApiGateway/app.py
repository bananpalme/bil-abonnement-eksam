from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Service URLs
RENTAL_SERVICE_URL = os.environ.get("RENTAL_SERVICE_URL", "http://localhost:5002")
ACCOUNT_SERVICE_URL = os.environ.get("ACCOUNT_SERVICE_URL", "http://localhost:5001")

# Rental Service routes

@app.route('/api/client', methods=['GET'])
def client_overview():
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.get(f"{RENTAL_SERVICE_URL}/client", headers=headers)
    try:
        data = response.json()
        return jsonify(data), response.status_code
    except ValueError:
        return response.text, response.status_code


@app.route('/api/client/<int:client_id>', methods=['GET'])
def client_by_id(client_id):
    response = requests.get(f"{RENTAL_SERVICE_URL}/client/{client_id}")
    return jsonify(response.json()), response.status_code


@app.route('/api/contract', methods=['POST'])
def make_contract():
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.post(f"{RENTAL_SERVICE_URL}/contract", json=request.get_json(), headers=headers)
    try:
        data = response.json()
        return jsonify(data), response.status_code
    except ValueError:
        return response.text, response.status_code


@app.route('/api/contract', methods=['GET'])
def see_contracts():
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.get(f"{RENTAL_SERVICE_URL}/contract", headers=headers)
    try:
        data = response.json()
        return jsonify(data), response.status_code
    except ValueError:
        return response.text, response.status_code


@app.route('/api/cars', methods=['GET'])
def cars():
    response = requests.get(f"{RENTAL_SERVICE_URL}/cars")
    return jsonify(response.json()), response.status_code


# Account service routes

@app.route('/api/profile', methods=['POST'])
def register():
    response = requests.post(f"{ACCOUNT_SERVICE_URL}/profile", json=request.get_json())
    return jsonify(response.json()), response.status_code


@app.route('/api/profile', methods=['GET'])
def view_profile():
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.get(f"{ACCOUNT_SERVICE_URL}/profile", headers=headers)
    return jsonify(response.json()), response.status_code


@app.route('/api/login', methods=['POST'])
def login():
    response = requests.post(f"{ACCOUNT_SERVICE_URL}/login",json=request.get_json())

    auth_header = response.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    data = response.json()

    role = data.get("role")
    username = data.get("username")
    
    return jsonify({
        "access_token": token,
        "role": role,
        "username": username
    }), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)