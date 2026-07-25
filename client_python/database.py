import sqlite3
from pathlib import Path
import os


ROOT = Path.cwd()
DB_PATH = ROOT / "database" / "client_logs.db"
# Dossier database à la racine du projet


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)
    




def init_database():
    """
    Initialise la base de données.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,

            level TEXT NOT NULL,

            module TEXT NOT NULL,

            message TEXT NOT NULL

        )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        current_session TEXT
    )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        client_id INTEGER,
        started_at TEXT,
        ended_at TEXT
    )
    """)

    conn.commit()

    
