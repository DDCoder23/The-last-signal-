import os
import re

from scripts.database_manager import DatabaseManager
from .utils import (read_report,
extract_int,extract_float)

REPORT_PATH = os.environ.get(
    "REPORT",
    "reports/rust-report.md"
)










def update_rust_database():

    report = read_report(REPORT_PATH)

    run_number = int(os.getenv("GITHUB_RUN_NUMBER", 0))
    branch = os.getenv("GITHUB_REF_NAME", "unknown")
    commit = os.getenv("GITHUB_SHA", "unknown")

    db = DatabaseManager()

    run_id = db.add_run(
        run_number,
        branch,
        commit
    )

    ##############################
    # Extraction des métriques
    ##############################

    clippy_warnings = extract_int(
        r"Clippy warnings:\s*(\d+)",
        report
    )

    cargo_tests = extract_int(
        r"Passed tests:\s*(\d+)",
        report
    )

    failed_tests = extract_int(
        r"Failed tests:\s*(\d+)",
        report
    )

    coverage = extract_float(
        r"Coverage:\s*([0-9.]+)",
        report
    )

    ##############################
    # Qualité
    ##############################

    db.add_quality(
        run_id,
        pylint=100 - clippy_warnings,
        coverage=coverage,
        complexity=0
    )

    ##############################
    # Tests
    ##############################

    db.cursor.execute(
        """
        INSERT INTO tests
        (
            run_id,
            total,
            passed,
            failed,
            skipped,
            duration
        )
        VALUES (?,?,?,?,?,?)
        """,
        (
            run_id,
            cargo_tests + failed_tests,
            cargo_tests,
            failed_tests,
            0,
            0
        )
    )

    db.connection.commit()
    db.close()

    print("Rust database updated")
