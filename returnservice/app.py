from flask import Flask, request, jsonify
from datetime import datetime
from database import CarReturn, get_db, init_db # Import af databasemodeller
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import os
# JWT setup
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('KEY')
jwt = JWTManager(app)

# --- Database Initialisering ---
# Sikrer at databasen og tabellerne er klar ved opstart.
with app.app_context():
    # Forsøg at initialisere DB (vigtigt ved Docker eller langsom opstart)
    max_retries = 5
    for i in range(max_retries):
        try:
            init_db()
            print("Database initialized successfully.")
            break
        except Exception as e:
            print(f"Error initializing database: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            if i == max_retries - 1:
                print("Failed to initialize database after multiple retries.")
                # raise # Fjern 'raise' hvis du vil fortsætte uden DB-forbindelse

# Helper funktion til at hente DB-session
def get_db_session():
    return next(get_db())

# =================================================================
# 1. Endpoint: Registrer Afleveringstidspunkt & Modtag Oplysninger (Trin 4)
# =================================================================
@app.route('/return/log', methods=['POST'])
def log_return():
    """
    Registrerer tidspunkt, nummerplade og kontrakt-ID, når kunden afleverer nøglen.
    """
    data = request.json
    
    if 'license_plate' not in data or 'contract_id' not in data:
        # Registrering af nødvendige oplysninger (Nummerplade og Kontrakt-ID)
        return jsonify({'error': 'Missing license_plate or contract_id'}), 400

    license_plate = data['license_plate']
    contract_id = data['contract_id']
    
    with get_db_session() as db:
        try:
            # Registrerer afleveringstidspunkt
            new_return = CarReturn(
                license_plate=license_plate,
                contract_id=contract_id,
                return_time=datetime.utcnow(), # Logger det præcise tidspunkt
                status='Key dropped in box'
            )
            
            db.add(new_return)
            db.commit()
            db.refresh(new_return)

            return jsonify({
                'message': 'Afleveringstidspunkt logget og gemt i DB.', 
                'return_id': new_return.id,
                'status': new_return.status
            }), 201

        except Exception as e:
            db.rollback()
            return jsonify({'error': f'Database error: {e}'}), 500


# =================================================================
# 2. Endpoint: Bekræft Nøgleafhentning (Trin 5)
# =================================================================
@app.route('/return/key_pickup', methods=['POST'])
@jwt_required()
def key_pickup():
    """
    Opdaterer status, når en medarbejder henter nøglen, og sender besked til kunden.
    """
    # tjekker at det er den rigtige rolle
    claims = get_jwt()
    role = claims.get("role")
    if role not in [ "dataregistry", "admin"]:
        return jsonify({"message": "Unnauthorized"}), 403

    data = request.json
    
    if 'employee_id' not in data or 'license_plate' not in data:
        return jsonify({'error': 'Missing employee_id or license_plate'}), 400

    employee_id = data['employee_id']
    license_plate = data['license_plate']

    with get_db_session() as db:
        try:
            # Find den seneste aflevering, der afventer afhentning
            car_return = db.query(CarReturn) \
                .filter(CarReturn.license_plate == license_plate) \
                .order_by(CarReturn.return_time.desc()) \
                .first()

            if not car_return:
                raise NoResultFound(f"No active return log found for license plate: {license_plate}")

            # Bekræfter nøgleafhentning: Opdater status og registrer medarbejder
            car_return.status = 'Key picked up by employee'
            car_return.employee_pickup_id = employee_id 
            db.commit()
            
            # Sender besked/notifikation til kunden
            notify_customer(license_plate)
            
            return jsonify({
                'message': f"Nøgle bekræftet af {employee_id}. Kunden er notificeret.",
                'new_status': car_return.status
            }), 200

        except NoResultFound as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            db.rollback()
            return jsonify({'error': f'Database error during pickup update: {e}'}), 500

def notify_customer(license_plate):
    """Simulerer afsendelse af digital bekræftelse til kunden."""
    # Dette simulerer systemets handling med at sende beskeden.
    print(f"--- NOTIFIKATION SENDT: Nøglen til {license_plate} er nu officielt modtaget af en medarbejder. ---")

if __name__ == '__main__':
    # Brug miljøvariabler så Docker kan styre host/port. Default lytter på 0.0.0.0:5000.
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0')
    # I dev kører vi med debug=True; i produktion bør dette være False.
    app.run(debug=True, host=host, port=port)