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


print("=== AVANT CREATION DU LOGGER FICHIER ===")
print("LOG DIR:", LOG_DIR.resolve())

if LOG_DIR.exists():
    files = list(LOG_DIR.iterdir())

    if files:
        for file in files:
            print(
                f"{file.name} - {file.stat().st_size} bytes"
            )
    else:
        print("Dossier logs vide.")
else:
    print("Dossier logs inexistant.")


#####################################
# Fichier avec rotation
#####################################

file_handler = RotatingFileHandler(
    filename=LOG_DIR / "the_last_signal.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    mode="a",
    encoding="utf-8",
    delay=False,
)


print("=== APRES CREATION DU LOGGER FICHIER ===")
print("LOG FILE:", file_handler.baseFilename)

print(
    "LOG SIZE:",
    Path(file_handler.baseFilename).stat().st_size
    if Path(file_handler.baseFilename).exists()
    else 0
)

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
print("CWD:", Path.cwd())
print("LOGGER HANDLERS:", logger.handlers)
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
        mode="a",
        encoding="utf-8",
        delay=False,
    )
    print("LOG FILE:", file_handler.baseFilename)
    print("LOG MODE:", file_handler.mode)
    print("LOG SIZE:", Path(file_handler.baseFilename).stat().st_size if Path(file_handler.baseFilename).exists() else 0)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    #####################################
    # SQLite
    #####################################

    sqlite_handler = SQLiteHandler()
    sqlite_handler.setLevel(logging.DEBUG)

    logger.addHandler(sqlite_handler)
