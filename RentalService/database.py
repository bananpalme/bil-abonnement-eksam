import sqlite3
import os

"""make db file in this path"""
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'rental_contracts.db')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create CLIENTS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)

    # Create CARS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            license_plate TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'available'
        )
    """)

    # Create RENTAL CONTRACTS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            months INTEGER NOT NULL,              
            monthly_rate REAL NOT NULL,
            total_cost REAL NOT NULL,           
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (car_id) REFERENCES cars(id)
        )
    """)

    """
        Dummy data
    """
    cursor.execute("SELECT COUNT(*) FROM clients")
    count = cursor.fetchone()[0]
    if count == 0:
        clients = [
            ("John", "Doe", "555-1234", "john.doe@example.com"),
            ("Emily", "Smith", "555-5678", "emily.smith@example.com"),
            ("Carlos", "Martinez", "555-9012", "carlos.martinez@example.com"),
            ("Anna", "Hansen", "555-3456", "anna.hansen@example.com"),
        ]
        cursor.executemany(
            "INSERT INTO clients (first_name, last_name, phone, email) VALUES (?, ?, ?, ?)",
            clients,
        )

    cursor.execute("SELECT COUNT(*) FROM cars")
    car_count = cursor.fetchone()[0]

    if car_count == 0:
        cars = [
            ("Toyota", "Corolla", 2020, "AB12345", "available"),
            ("Toyota", "RAV4", 2021, "CD67890", "rented"),
            ("Honda", "Civic", 2019, "EF11223", "available"),
            ("Honda", "CR-V", 2022, "GH44556", "maintenance"),
            ("Ford", "Focus", 2018, "IJ77889", "available"),
            ("Ford", "Kuga", 2020, "KL99001", "available"),
            ("BMW", "320i", 2021, "MN22334", "rented"),
            ("BMW", "X3", 2022, "OP55667", "available"),
            ("Mercedes", "A200", 2019, "QR88990", "available"),
            ("Mercedes", "GLA250", 2021, "ST11224", "available"),
        ]

        cursor.executemany(
            "INSERT INTO cars (make, model, year, license_plate, status) VALUES (?, ?, ?, ?, ?)",
            cars
        )
        
    ''' If you need to delete duplicates
    cursor.execute("""
        DELETE FROM clients
        WHERE id NOT IN (
            SELECT id FROM (
                SELECT MIN(id) as id
                FROM clients
                GROUP BY first_name, last_name
            )
        )
    """)
    '''

    conn.commit()
    conn.close()



def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()

    conn.close()

    return [
        {
            'id': client['id'],
            'first_name': client['first_name'],
            'last_name': client['last_name']
        }
        for client in clients
    ]

def get_cars():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()

    conn.close()
    
    return [
        {
            'id': car['id'],
            'make': car['make'],
            'model': car['model'],
            'year': car['year'],
            'status': car['status']
        }
        for car in cars
    ]

def get_client_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clients WHERE first_name = ?', (name,))

    clients = cursor.fetchall()

    conn.close()
    
    return [
        {
            'id': client['id'],
            'first_name': client['first_name'],
            'last_name': client['last_name']
        }
        for client in clients
    ]

def make_new_contract(client_id, car_id, months, daily_rate, total_cost):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO rentals (client_id, car_id, months, daily_rate, total_cost) VALUES (?, ?, ?, ?, ?)'
                   , (client_id, car_id, months, daily_rate, total_cost))

    conn.commit()

    conn.close()
    
def get_all_contracts():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM rentals')
    contracts = cursor.fetchall()

    conn.close()

    return [
        {
            'client_id': cont['client_id'],
            'car_id': cont['car_id'],
            'months': cont['months'],
            'daily_rate': cont['daily_rate'],
            'total_cost': cont['total_cost']
        }
        for cont in contracts
    ]


init_database()