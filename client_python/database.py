import sqlite3
from pathlib import Path

# Dossier database à la racine du projet
DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "client_logs.db"


def get_connection():
    """
    Retourne une connexion SQLite.
    """
    return sqlite3.connect(DB_PATH)


def init_database():
    """
    Initialise la base de données.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            level TEXT NOT NULL,

            module TEXT NOT NULL,

            message TEXT NOT NULL

        )
    """)

    conn.commit()

    
