from datetime import datetime

from .database import get_connection


def add_log(
    session_id: str,
    level: str,
    module: str,
    message: str,
):
    """
    Ajoute un log dans la base.
    """

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO logs (
                session_id,
                timestamp,
                level,
                module,
                message
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session_id,
                datetime.now().isoformat(timespec="seconds"),
                level,
                module,
                message,
            ),
        )

        conn.commit()

    finally:
        conn.close()
def get_last_logs(limit=100):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()

    finally:
        conn.close()
def get_logs_by_session(session_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM logs
            WHERE session_id = ?
            ORDER BY id
            """,
            (session_id,),
        )

        return cursor.fetchall()

    finally:
        conn.close()
from pathlib import Path

from .database import get_connection

LOG_FILE = Path("logs/the_last_signal.log")
LOG_DIR = Path("logs")


def clear_logs():
    """
    Supprime tous les logs de la base SQLite
    et vide le fichier de logs.
    """

    # SQLite
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logs")
        conn.commit()

    finally:
        conn.close()

    # Fichier .log
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LOG_DIR.exists():
        for log_file in LOG_DIR.glob("*.log"):
            log_file.unlink(missing_ok=True)

        # Supprime aussi les fichiers de rotation :
        # the_last_signal.log.1, .2, etc.
        for log_file in LOG_DIR.glob("*.log.*"):
            log_file.unlink(missing_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8"):
        pass


    
