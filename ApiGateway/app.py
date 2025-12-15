from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Service URLs
RENTAL_SERVICE_URL = os.environ.get("RENTAL_SERVICE_URL", "http://localhost:5001")
INSPECTION_SERVICE_URL = os.environ.get("INSPECTION_SERVICE_URL", "http://localhost:5005")


# Rental Service routes
@app.route('/api/client', methods=['GET'])
def client_overview():
    try:
        response = requests.get(f"{RENTAL_SERVICE_URL}/client", timeout=10)
        data = response.json()
        return jsonify(data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to rental service: {str(e)}"}), 503

@app.route('/api/client/<int:client_id>', methods=['GET'])
def client_by_id(client_id):
    response = requests.get(f"{RENTAL_SERVICE_URL}/client/{client_id}")
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
    try:
        response = requests.get(f"{RENTAL_SERVICE_URL}/cars", timeout=10)
        data = response.json()
        return jsonify(data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to rental service: {str(e)}"}), 503

# Inspection Service routes
@app.route('/api/inspection', methods=['POST'])
def create_inspection():
    response = requests.post(f"{INSPECTION_SERVICE_URL}/inspection", json=request.get_json())
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/inspection/<int:id>', methods=['GET'])
def get_inspection(id):
    response = requests.get(f"{INSPECTION_SERVICE_URL}/inspection/{id}")
    data = response.json()

    return jsonify(data), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)