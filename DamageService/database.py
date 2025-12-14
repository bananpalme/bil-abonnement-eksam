import sqlite3
import os

"""make db file in this path"""
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'damage.db')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Damages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS damage_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            base_cost REAL NOT NULL
        )
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_damages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            damage_type_id INTEGER NOT NULL,
            cost_at_time REAL
        )
    """)

    # dummy data

    cursor.execute("SELECT COUNT(*) FROM damage_types")
    count = cursor.fetchone()[0]
    if count == 0:
        damages = [
            ("Scratch", 250 ),
            ("Dent", 450),
            ("Broken mirror", 450),
            ("Cracked windshield", 1200),
            ("Broken headlight", 650),
            ("Suspension damage", 500),
            ("Dashboard damage", 1200),
            ("Seat stain", 200),
            ("Transmission damage", 3250),
            ("Brake system damage", 1680)
        ]
        cursor.executemany(
            "INSERT INTO damage_types (name, base_cost) VALUES (?, ?)",
            damages,
        )

    conn.commit()
    conn.close()

def get_all_damage_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage_types')
    damages = cursor.fetchall()
    conn.close()
    return [{"id": d["id"], "name": d["name"], "base_cost": d["base_cost"]} for d in damages]

def update_car_damages(damage_list):
    conn = get_db_connection()
    cursor = conn.cursor()
    for d in damage_list:
        cursor.execute(
            "INSERT INTO car_damages (car_id, damage_type_id, cost_at_time) VALUES (?, ?, ?)",
            (d["car_id"], d["damage_type_id"], d["cost_at_time"])
        )
    conn.commit()
    conn.close()

def get_all_car_damages():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM car_damages')
    car_damages = cursor.fetchall()

    conn.close()

    return [
        {
            'id': damage['id'],
            'car_id': damage['car_id'],
            'damage_type_id': damage['damage_type_id'],
            'cost_at_time': damage['cost_at_time']
        }
        for damage in car_damages
    ]

def get_car_damages_totals():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Join car_damages with damage_types to get names and costs
    cursor.execute("""
        SELECT car_damages.car_id, damage_types.name AS damage_name, car_damages.cost_at_time
        FROM car_damages
        JOIN damage_types ON car_damages.damage_type_id = damage_types.id
    """)
    rows = cursor.fetchall()
    conn.close()

    # Aggregate by car_id
    result = {}
    for row in rows:
        car_id = row['car_id']
        damage_name = row['damage_name']
        cost = row['cost_at_time']

        if car_id not in result:
            result[car_id] = {
                'car_id': car_id,
                'damages': [],
                'total_cost': 0
            }
        
        result[car_id]['damages'].append({
            'name': damage_name,
            'cost_at_time': cost
        })
        result[car_id]['total_cost'] += cost

    return list(result.values())

init_database()