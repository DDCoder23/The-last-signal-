import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
import traceback
from .session import SessionContext
from .database import get_connection, init_database
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
        print(
            "SQLite reçoit :",
            record.getMessage()
        )
        
        try:
            cursor = conn.cursor()

            cursor.execute("""
             INSERT INTO logs (
             session_id,
             timestamp,
             level,
             module,
            message
              )
           VALUES (?, ?, ?, ?, ?)
           """, (
    SessionContext.session_id,
    datetime.now().isoformat(timespec="seconds"),
    record.levelname,
    record.name,
    record.getMessage(),
))

            conn.commit()
        except Exceptions: 
            print(traceback.format_exc)
            

        finally:
            conn.close()


logger = logging.getLogger("TheLastSignal")
logger.setLevel(logging.DEBUG)
logger.propagate = False
logger.handlers.clear()
formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
)

print("CWD:", Path.cwd())
print("LOGGER HANDLERS:", logger.handlers)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler = RotatingFileHandler(
        filename=LOG_DIR / "the_last_signal.log",
        maxBytes= 10 * 1024 * 1024,  # 5 Mo
        backupCount=10000000000,
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
sqlite_handler = SQLiteHandler()
sqlite_handler.setLevel(logging.DEBUG)
logger.addHandler(sqlite_handler)
