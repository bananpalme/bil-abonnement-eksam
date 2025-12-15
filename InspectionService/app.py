from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import get_db_connection
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('KEY')
jwt = JWTManager(app)

@app.route("/inspection", methods=["POST"])
@jwt_required()
def create_inspection():

    claims = get_jwt()
    role = claims.get("role")
    if role not in ["damages", "admin"]:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO inspections 
        (car_number, car_model, km_before, km_after,
         seats_ok, steering_ok, carpet_ok, belts_ok, gearbox_ok, smell_ok, warning_lights_ok,
         date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("car_number"),
        data.get("car_model"),
        data.get("km_before"),
        data.get("km_after"),
        data.get("seats_ok"),
        data.get("steering_ok"),
        data.get("carpet_ok"),
        data.get("belts_ok"),
        data.get("gearbox_ok"),
        data.get("smell_ok"),
        data.get("warning_lights_ok"),
        data.get("date")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Inspection saved!"}), 201


@app.route("/inspection/<int:id>", methods=["GET"])
def get_inspection(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM inspections WHERE id = ?", (id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Inspection not found"}), 404

    return jsonify(dict(row)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
