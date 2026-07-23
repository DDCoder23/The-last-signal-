import sqlite3


def voir_database(DB):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")
    tables = cursor.fetchall()
    print("=" * 60)
    print("TABLES")
    print("=" * 60)
    for (table,) in tables:
        print("-", table)
    for (table,) in tables:
        print("\n" + "=" * 60)
        print(table.upper())
        print("=" * 60)
        # Colonnes
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [c[1] for c in cursor.fetchall()]
        print("Colonnes :")
        print(columns)
        # Données
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        print(f"\nNombre de lignes : {len(rows)}")
        for row in rows:
            print(row)
    conn.close()
