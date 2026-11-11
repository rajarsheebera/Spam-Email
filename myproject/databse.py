import sqlite3
from pathlib import Path

Base_dir = Path(r"C:\Users\HP\Downloads\archive (7)\spam.csv").resolve().parent
Database_path=Base_dir/"spm_history.db"

def get_connection():
    connection = sqlite3.connect(Database_path)
    connection.row_factory=sqlite3.Row
    return connection
def create_table():
    connection = get_connection()
    try:
        cursor =connection.cursor()

        cursor.execute("""
               CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            prediction TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
""")
        connection.commit()
    finally:
        connection.close()
def save_prediction(message,prediction):
    connection =get_connection()
    try:
        cursor =connection.cursor()

        cursor.execute("""
        INSERT INTO predictions (message, prediction)
        VALUES (?, ?)
""",(message,prediction))
        connection.commit()
    finally:
        connection.close()
def get_prediction_history():
    connection=get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, message, prediction, created_at
        FROM predictions
        ORDER BY id DESC
""")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


  




        
