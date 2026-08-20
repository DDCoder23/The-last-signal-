import shutil
import sqlite3
import tempfile
from pathlib import Path

import pytest


DATABASE_PATH = (
    Path(__file__).resolve().parents[2]
    / "database_test"
    / "the_last_signal.db"
)


SENSITIVE_TABLES = {
    "users",
    "accounts",
    "clients",
    "sessions",
}


SQL_INJECTION_PAYLOADS = [
    "'",
    '"',
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    '" OR 1=1 --',
    "admin'--",
    "admin' OR '1'='1",
    "Dev'--",
    "Dev' OR '1'='1",
    "SuperDev'--",
    "SuperDev' OR '1'='1",
    "' UNION SELECT NULL --",
    "' UNION SELECT * FROM users --",
    "'; DROP TABLE users; --",
    "'; DROP TABLE accounts; --",
    "'; DROP TABLE permissions; --",
    
]
def open_database(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection
def get_tables(connection: sqlite3.Connection) -> list[str]:
    cursor = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )

    return [row[0] for row in cursor.fetchall()]
def check_integrity(connection: sqlite3.Connection) -> str:
    result = connection.execute(
        "PRAGMA integrity_check;"
    ).fetchone()

    if result is None:
        return "no result"

    return result[0]
def check_foreign_keys(
    connection: sqlite3.Connection,
) -> list[tuple]:
    return connection.execute(
        "PRAGMA foreign_key_check;"
    ).fetchall()
def get_table_schema(
    connection: sqlite3.Connection,
    table: str,
) -> list[tuple]:
    return connection.execute(
        f'PRAGMA table_info("{table}");'
    ).fetchall()
def get_row_count(
    connection: sqlite3.Connection,
    table: str,
) -> int:
    result = connection.execute(
        f'SELECT COUNT(*) FROM "{table}";'
    ).fetchone()

    return int(result[0])
def create_test_database() -> tuple[Path, tempfile.TemporaryDirectory]:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database introuvable : {DATABASE_PATH}"
        )

    temporary_directory = tempfile.TemporaryDirectory()

    temporary_path = (
        Path(temporary_directory.name)
        / "the_last_signal_attack.db"
    )

    shutil.copy2(
        DATABASE_PATH,
        temporary_path,
    )

    return temporary_path, temporary_directory
def attack_delete(
    connection: sqlite3.Connection,
    table: str,
) -> tuple[bool, str]:

    try:
        connection.execute(
            f'DELETE FROM "{table}";'
        )

        connection.commit()

        return True, "DELETE accepté"

    except sqlite3.Error as error:
        connection.rollback()

        return False, str(error)
def attack_drop_table(
    connection: sqlite3.Connection,
    table: str,
) -> tuple[bool, str]:

    try:
        connection.execute(
            f'DROP TABLE "{table}";'
        )

        connection.commit()

        return True, "DROP TABLE accepté"

    except sqlite3.Error as error:
        connection.rollback()

        return False, str(error)
def attack_update(
    connection: sqlite3.Connection,
    table: str,
) -> tuple[bool, str]:

    try:
        columns = get_table_schema(
            connection,
            table,
        )

        if not columns:
            return False, "Aucune colonne"

        column = columns[0][1]

        connection.execute(
            f'''
            UPDATE "{table}"
            SET "{column}" = NULL;
            '''
        )

        connection.commit()

        return True, f"UPDATE {column}=NULL accepté"

    except sqlite3.Error as error:
        connection.rollback()

        return False, str(error)
def attack_invalid_insert(
    connection: sqlite3.Connection,
    table: str,
) -> tuple[bool, str]:

    try:
        columns = get_table_schema(
            connection,
            table,
        )

        if not columns:
            return False, "Aucune colonne"

        column_names = [
            column[1]
            for column in columns
        ]

        placeholders = ", ".join(
            "?"
            for _ in column_names
        )

        values = [
            None
            for _ in column_names
        ]

        connection.execute(
            f'''
            INSERT INTO "{table}"
            ({", ".join(f'"{column}"' for column in column_names)})
            VALUES ({placeholders});
            ''',
            values,
        )

        connection.commit()

        return True, "INSERT NULL accepté"

    except sqlite3.Error as error:
        connection.rollback()

        return False, str(error)
def attack_large_value(
    connection: sqlite3.Connection,
    table: str,
) -> tuple[bool, str]:

    try:
        columns = get_table_schema(
            connection,
            table,
        )

        if not columns:
            return False, "Aucune colonne"

        column = columns[0][1]

        gigantic_value = "A" * 1_000_000

        connection.execute(
            f'''
            UPDATE "{table}"
            SET "{column}" = ?;
            ''',
            (gigantic_value,),
        )

        connection.commit()

        return True, "Valeur de 1 MB acceptée"

    except sqlite3.Error as error:
        connection.rollback()

        return False, str(error)
def test_payload_as_parameter(
    connection: sqlite3.Connection,
    payload: str,
) -> tuple[bool, str]:

    try:
        connection.execute(
            """
            SELECT ?
            """,
            (payload,),
        ).fetchone()

        return True, "Payload traité comme donnée"

    except sqlite3.Error as error:
        return False, str(error)
def verify_database(
    connection: sqlite3.Connection,
) -> tuple[str, list[tuple]]:

    integrity = check_integrity(connection)

    foreign_keys = check_foreign_keys(connection)

    return integrity, foreign_keys
@pytest.mark.security
def test_sql_injection():
    print("\n")
    print("=" * 70)
    print("SQL / DATABASE SECURITY DESTROYER")
    print("=" * 70)

    test_database, temporary_directory = create_test_database()

    print(f"\nOriginal : {DATABASE_PATH}")
    print(f"Test     : {test_database}")

    try:
        connection = open_database(test_database)

        try:
            # ==========================================================
            # BASELINE
            # ==========================================================

            print("\n[BASELINE]")

            integrity = check_integrity(connection)

            print(f"SQLite integrity : {integrity}")

            assert integrity == "ok", (
                f"Database de test déjà corrompue : {integrity}"
            )

            tables = get_tables(connection)

            print(f"Tables détectées : {len(tables)}")

            assert tables, "Aucune table détectée."

            for table in tables:
                row_count = get_row_count(
                    connection,
                    table,
                )

                marker = (
                    "SENSITIVE"
                    if table in SENSITIVE_TABLES
                    else "NORMAL"
                )

                print(
                    f"[{marker}] "
                    f"{table}: "
                    f"{row_count} ligne(s)"
                )

            # ==========================================================
            # FOREIGN KEYS
            # ==========================================================

            print("\n[FOREIGN KEYS]")

            foreign_keys = check_foreign_keys(connection)

            if foreign_keys:
                print(
                    "❌ Violations détectées :"
                )

                for violation in foreign_keys:
                    print(
                        f"    {violation}"
                    )

                pytest.fail(
                    "La database possède déjà "
                    "des violations de clés étrangères."
                )

            print("✅ Aucune violation")

            # ==========================================================
            # SQL INJECTION PAYLOADS
            # ==========================================================

            print("\n[SQL INJECTION PAYLOADS]")

            for payload in SQL_INJECTION_PAYLOADS:

                success, result = test_payload_as_parameter(
                    connection,
                    payload,
                )

                if success:
                    print(
                        f"[SAFE] {payload!r} "
                        f"-> {result}"
                    )
                else:
                    print(
                        f"[ERROR] {payload!r} "
                        f"-> {result}"
                    )

            # ==========================================================
            # DESTRUCTIVE TESTS
            # ==========================================================

            print("\n[DESTRUCTIVE TESTS]")

            for table in tables:

                print(
                    f"\n--- {table} ---"
                )

                # ------------------------------------------------------
                # DELETE
                # ------------------------------------------------------

                delete_success, delete_result = attack_delete(
                    connection,
                    table,
                )

                print(
                    f"DELETE : "
                    f"{'ACCEPTED' if delete_success else 'BLOCKED'} "
                    f"({delete_result})"
                )

                # ------------------------------------------------------
                # DROP
                # ------------------------------------------------------

                drop_success, drop_result = attack_drop_table(
                    connection,
                    table,
                )

                print(
                    f"DROP   : "
                    f"{'ACCEPTED' if drop_success else 'BLOCKED'} "
                    f"({drop_result})"
                )

                # ------------------------------------------------------
                # La table peut avoir été détruite.
                # On ne continue donc pas les attaques dessus.
                # ------------------------------------------------------

                remaining_tables = get_tables(
                    connection,
                )

                if table not in remaining_tables:
                    print(
                        "⚠️ TABLE DÉTRUITE "
                        f"par DROP : {table}"
                    )

                    break

                # ------------------------------------------------------
                # UPDATE NULL
                # ------------------------------------------------------

                update_success, update_result = attack_update(
                    connection,
                    table,
                )

                print(
                    f"UPDATE : "
                    f"{'ACCEPTED' if update_success else 'BLOCKED'} "
                    f"({update_result})"
                )

                # ------------------------------------------------------
                # INSERT NULL
                # ------------------------------------------------------

                insert_success, insert_result = (
                    attack_invalid_insert(
                        connection,
                        table,
                    )
                )

                print(
                    f"INSERT : "
                    f"{'ACCEPTED' if insert_success else 'BLOCKED'} "
                    f"({insert_result})"
                )

                # ------------------------------------------------------
                # LARGE VALUE
                # ------------------------------------------------------

                large_success, large_result = attack_large_value(
                    connection,
                    table,
                )

                print(
                    f"1MB    : "
                    f"{'ACCEPTED' if large_success else 'BLOCKED'} "
                    f"({large_result})"
                )

            # ==========================================================
            # FINAL INTEGRITY
            # ==========================================================

            print("\n[FINAL INTEGRITY]")

            final_integrity, final_foreign_keys = (
                verify_database(connection)
            )

            print(
                f"SQLite integrity : "
                f"{final_integrity}"
            )

            print(
                f"Foreign key violations : "
                f"{len(final_foreign_keys)}"
            )

            print("\n" + "=" * 70)
            print("DESTROYER FINISHED")
            print("=" * 70)

        finally:
            connection.close()

    finally:
        temporary_directory.cleanup()
