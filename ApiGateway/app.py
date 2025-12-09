from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Service URLs
RENTAL_SERVICE_URL = os.environ.get("RENTAL_SERVICE_URL", "http://localhost:5001")


# Rental Service routes
@app.route('/api/client', methods=['GET'])
def client_overview():
    response = requests.get(f"{RENTAL_SERVICE_URL}/client")
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/contract', methods=['POST'])
def make_contract():
    response = requests.post(f"{RENTAL_SERVICE_URL}/contract", json=request.get_json())
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/contract', methods=['GET'])
def see_contracts():
    response = requests.get(f"{RENTAL_SERVICE_URL}/contract")
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/cars', methods=['GET'])
def cars():
    response = requests.get(f"{RENTAL_SERVICE_URL}/cars")
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/rental', methods=['GET'])
def rental():
    response = requests.get(f"{RENTAL_SERVICE_URL}/cars")
    data = response.json()

    return jsonify(data), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)