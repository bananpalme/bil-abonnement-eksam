import sqlite3

# Opret forbindelse til databasen (filen bliver lavet automatisk hvis den ikke findes)
def get_db_connection():
    conn = sqlite3.connect('inspection.db')
    conn.row_factory = sqlite3.Row  # gør det nemt at læse data som dict
    return conn

# Opret tabellen hvis den ikke findes
def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_number TEXT,
            car_model TEXT,
            km_before INTEGER,
            km_after INTEGER,

            seats_ok BOOLEAN,
            steering_ok BOOLEAN,
            carpet_ok BOOLEAN,
            belts_ok BOOLEAN,
            gearbox_ok BOOLEAN,
            smell_ok BOOLEAN,
            warning_lights_ok BOOLEAN,

            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Kør kun når filen startes direkte
if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")
    
