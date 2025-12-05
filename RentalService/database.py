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
            daily_rate REAL NOT NULL,
            total_cost REAL NOT NULL,           
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (car_id) REFERENCES cars(id)
        )
    """)

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



init_database()