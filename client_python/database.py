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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Nombre de tables : {len(tables)}")
    for (table_name,) in tables:
        print("\n" + "=" * 60)
        print(f"TABLE : {table_name}")
        print("=" * 60)
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print("Colonnes :")
        for col in columns:
            print(col)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\nNombre de lignes : {len(rows)}")
        for row in rows:
            print(row)


    return conn


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

    
