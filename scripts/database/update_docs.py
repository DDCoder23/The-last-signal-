import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database_manager import DatabaseManager


def update_docs_database():

    score = Path("reports/docs/score.txt")

    problems = Path("reports/docs/problems.json")

    if not score.exists():
        return

    score = int(score.read_text())

    if problems.exists():

        data = json.loads(
            problems.read_text(
                encoding="utf-8"
            )
        )

        errors = sum(
            p["severity"] == "error"
            for p in data
        )

        warnings = sum(
            p["severity"] == "warning"
            for p in data
        )

    else:

        errors = 0
        warnings = 0

    db = DatabaseManager()

    run = db.add_run(...)

    db.cursor.execute(
        """
        INSERT INTO documentation
        (
            run_id,
            score,
            errors,
            warnings
        )

        VALUES (?,?,?,?)
        """,

        (
            run,
            score,
            errors,
            warnings
        )
    )

    db.connection.commit()

    db.close()
