import os
import re

from .utils import (
    read_report,
    extract_float,
    extract_int,
)



REPORT_PATH = os.environ.get(
    "REPORT",
    "reports/python/python-report.md"
)


def update_python_database(db):

    report = read_report(REPORT_PATH)

    if not report:
        print("Python report not found.")
        return

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

    

    run_id = db.add_run(
        run_number,
        branch,
        commit
    )

    # ==========================================
    # Quality metrics
    # ==========================================

    pylint = extract_float(
        r"Your code has been rated at ([0-9.]+)",
        report
    )

    coverage = extract_float(
        r"TOTAL.*?(\d+)%",
        report
    )

    complexity = extract_float(
        r"Average complexity.*?([0-9.]+)",
        report
    )

    db.insert(
        "quality_metrics",
        run_id=run_id,
        pylint=pylint,
        coverage=coverage,
        complexity=complexity,
        documentation=0
    )

    # ==========================================
    # Test summary
    # ==========================================

    passed = extract_int(
        r"passed=(\d+)",
        report
    )

    failed = extract_int(
        r"failed=(\d+)",
        report
    )

    skipped = extract_int(
        r"skipped=(\d+)",
        report
    )

    duration = extract_float(
        r"=+\s*([0-9.]+)\s*seconds\s*=+",
        report
    )

    db.insert(
        "test_summary",
        run_id=run_id,
        total=passed + failed + skipped,
        passed=passed,
        failed=failed,
        skipped=skipped,
        duration=duration
    )

    # ==========================================
    # Flake8
    # ==========================================

    flake_pattern = re.compile(
        r"^(.*?):(\d+):(\d+): ([A-Z]\d+) (.+)$",
        re.MULTILINE
    )

    for file, line, column, code, message in flake_pattern.findall(report):

        db.insert(
            "flake8_errors",
            run_id=run_id,
            file=file,
            line=int(line),
            column_number=int(column),
            code=code,
            message=message
        )

    # ==========================================
    # Black
    # ==========================================

    black_pattern = re.compile(
        r"(reformatted|would reformat|left unchanged)\s+(.+)"
    )

    for status, file in black_pattern.findall(report):

        db.insert(
            "black_files",
            run_id=run_id,
            file=file,
            status=status
        )

    # ==========================================
    # Pytest details
    # ==========================================

    pytest_pattern = re.compile(
        r"([^\s]+)\s+(PASSED|FAILED|SKIPPED)"
    )

    for test_name, status in pytest_pattern.findall(report):

        db.insert(
            "pytest_results",
            run_id=run_id,
            test_name=test_name,
            status=status,
            duration=0,
            error=""
        )

    

    print("Python database updated successfully.")
