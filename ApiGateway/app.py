from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Service URLs
RENTAL_SERVICE_URL = os.environ.get("RENTAL_SERVICE_URL", "http://localhost:5001")
Return_SERVICE_URL = os.environ.get("RETURN_SERVICE_URL", "http://localhost:5002")


# Rental Service routes
@app.route('/api/client', methods=['GET'])
def client_overview():
    response = requests.get(f"{RENTAL_SERVICE_URL}/client")
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/cars', methods=['GET'])
def cars():
    response = requests.get(f"{RENTAL_SERVICE_URL}/cars")
    data = response.json()

    return jsonify(data), response.status_code
     # Return Service routes
@app.route('/api/return/log', methods=['POST'])
def log_return():

    response = requests.post(f"{Return_SERVICE_URL}/return/log", json=request.json)
    data = response.json()

    return jsonify(data), response.status_code

@app.route('/api/return/key_pickup', methods=['POST'])
def key_pickup():
    response = requests.post(f"{Return_SERVICE_URL}/return/key_pickup", json=request.json)
    data = response.json()

    return jsonify(data), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

   