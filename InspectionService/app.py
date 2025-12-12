from flask import Flask, request, jsonify
from database import get_db_connection

app = Flask(__name__)

@app.route("/inspection", methods=["POST"])
def create_inspection():
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
    app.run(host="0.0.0.0", port=5002)
