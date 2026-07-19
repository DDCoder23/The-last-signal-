import os
import re


from .utils import read_report

REPORT_PATH = os.environ.get(
    "REPORT",
    "reports/security/security-report.md"
)


def update_security_database(db):

    report = read_report(REPORT_PATH)

    run_number = int(os.getenv("GITHUB_RUN_NUMBER", 0))
    branch = os.getenv("GITHUB_REF_NAME", "unknown")
    commit = os.getenv("GITHUB_SHA", "unknown")

    

    run_id = db.add_run(
        run_number,
        branch,
        commit
    )

    ###########################################
    # Résumé général
    ###########################################

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

    db.add_security(
        run_id,
        high,
        medium,
        low,
        total,
        files
    )

    ###########################################
    # Détails des vulnérabilités
    ###########################################

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

        db.add_security_issue(
            run_id=run_id,
            test=test.strip(),
            severity=severity.strip(),
            confidence=confidence.strip(),
            cwe=cwe.strip(),
            info=info.strip(),
            file=file.strip(),
            line=int(line),
            column=int(column),
        )

    db.close()

    print("Security database updated successfully")
