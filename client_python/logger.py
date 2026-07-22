import logging
from datetime import datetime

from .database import init_database
from .database import get_connection

# Création de la base si elle n'existe pas
init_database()


class SQLiteHandler(logging.Handler):
    """
    Handler qui enregistre les logs dans SQLite.
    """

    def emit(self, record):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO logs(
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
        conn.close()


logger = logging.getLogger("TheLastSignal")

logger.setLevel(logging.DEBUG)

# Evite les doublons si le module est importé plusieurs fois
if not logger.handlers:

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s",
        "%H:%M:%S"
    )

    #####################################
    # Console
    #####################################

    console = logging.StreamHandler()

    console.setFormatter(formatter)

    logger.addHandler(console)

    #####################################
    # SQLite
    #####################################

    sqlite = SQLiteHandler()

    sqlite.setFormatter(formatter)

    logger.addHandler(sqlite)
