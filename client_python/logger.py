import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

from .database import get_connection, init_database

# Création de la base si elle n'existe pas
init_database()

# Création du dossier des logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


class SQLiteHandler(logging.Handler):
    """
    Handler qui enregistre les logs dans SQLite.
    """

    def emit(self, record):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO logs (
                    timestamp,
                    level,
                    module,
                    message
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    datetime.now().isoformat(timespec="seconds"),
                    record.levelname,
                    record.name,
                    record.getMessage(),
                ),
            )

            conn.commit()

        finally:
            conn.close()


logger = logging.getLogger("TheLastSignal")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Évite les doublons si le module est importé plusieurs fois
if not logger.handlers:

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    #####################################
    # Console
    #####################################

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    #####################################
    # Fichier avec rotation
    #####################################

    file_handler = RotatingFileHandler(
        filename=LOG_DIR / "the_last_signal.log",
        maxBytes=5 * 1024 * 1024,  # 5 Mo
        backupCount=5,
        encoding="utf-8",
        delay=True,
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    #####################################
    # SQLite
    #####################################

    sqlite_handler = SQLiteHandler()
    sqlite_handler.setLevel(logging.DEBUG)

    logger.addHandler(sqlite_handler)
