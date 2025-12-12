import sqlite3
import os

"""make db file in this path"""
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'accounts.db')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    #create accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('dataregistry', 'damages', 'admin'))
        )
    """)

    conn.commit()
    conn.close()

def add_account(username, password, role):
    # make a new account in the database
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO accounts (username, password, role) VALUES (?, ?, ?)',
        (username, password, role)
    )

    conn.commit()
    conn.close()

    return {
        'username': username,
        'password': password,
        'role': role
    }

def find_account_by_username(username):
    """Find an account by their username"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
    account = cursor.fetchone()

    conn.close()

    if account:
        return {
            'id': account['id'],
            'username': account['username'],
            'password': account['password'],
            'role': account['role']
        }
    return None

init_database()