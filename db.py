
import sqlite3
import os

def get_connection():
    path = os.path.join(os.path.dirname(__file__), 'users.db')
    return sqlite3.connect(path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            face_descriptor BLOB
        )
    ''')
    conn.commit()
    conn.close()
