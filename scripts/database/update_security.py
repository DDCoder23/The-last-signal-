import os
import re
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database_manager import DatabaseManager
from utils import read_report
REPORT_PATH = os.environ.get(
    "REPORT",
    "reports/security-report.md"
)





def update_security_database():

    report = read_report(REPORT_PATH)

    run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 0))
    branch = os.environ.get("GITHUB_REF", "unknown")
    commit = os.environ.get("GITHUB_SHA", "unknown")

    db = DatabaseManager()

    run_id = db.add_run(
        run_number,
        branch,
        commit
    )

    # ----------------------------
    # Statistiques générales
    # ----------------------------

    high = len(re.findall(r"Severity:\s*High", report))
    medium = len(re.findall(r"Severity:\s*Medium", report))
    low = len(re.findall(r"Severity:\s*Low", report))

    total = high + medium + low

    files = len(
        set(
            re.findall(
                r"Location:\s*(.+?):\d+:\d+",
                report
            )
        )
    )

    db.cursor.execute(
        """
        INSERT INTO security
        (
            run_id,
            high,
            medium,
            low,
            total,
            files
        )
        VALUES (?,?,?,?,?,?)
        """,
        (
            run_id,
            high,
            medium,
            low,
            total,
            files
        )
    )

    # ----------------------------
    # Détails des vulnérabilités
    # ----------------------------

    pattern = re.compile(
        r">> Issue: \[(.*?)\].*?"
        r"Severity:\s*(.*?)\s+"
        r"Confidence:\s*(.*?)\s+"
        r"CWE:\s*(.*?)\s+\("
        r".*?"
        r"More Info:\s*(.*?)\n"
        r".*?"
        r"Location:\s*(.*?):(\d+):(\d+)",
        re.S
    )

    for (
        test,
        severity,
        confidence,
        cwe,
        info,
        file,
        line,
        column
    ) in pattern.findall(report):

        db.cursor.execute(
            """
            INSERT INTO security_issues
            (
                run_id,
                test,
                severity,
                confidence,
                cwe,
                info,
                file,
                line,
                column
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                run_id,
                test.strip(),
                severity.strip(),
                confidence.strip(),
                cwe.strip(),
                info.strip(),
                file.strip(),
                int(line),
                int(column),
            )
        )

    db.connection.commit()
    db.close()

    print("Security database updated successfully")



