import json
import os
from pathlib import Path

from ..database_manager import DatabaseManager


def update_docs_database():

    score_file = Path("reports/docs/score.txt")
    problems_file = Path("reports/docs/problems.json")

    if not score_file.exists():
        return

    score = int(score_file.read_text().strip())

    errors = 0
    warnings = 0

    if problems_file.exists():

        data = json.loads(
            problems_file.read_text(
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

    run_number = int(
        os.environ.get(
            "GITHUB_RUN_NUMBER",
            0
        )
    )

    branch = os.environ.get(
        "GITHUB_REF",
        "unknown"
    )

    commit = os.environ.get(
        "GITHUB_SHA",
        "unknown"
    )

    db = DatabaseManager()

    run_id = db.add_run(
        run_number,
        branch,
        commit
    )

    db.insert(
        "documentation_summary",
        run_id=run_id,
        score=score,
        errors=errors,
        warnings=warnings
    )

    if problems_file.exists():

        for problem in data:

            db.insert(
                "doc_problems",
                run_id=run_id,
                file=problem.get("file", ""),
                severity=problem.get("severity", ""),
                module=problem.get("module", ""),
                message=problem.get("message", "")
            )

    db.close()

    print("Documentation database updated successfully")
