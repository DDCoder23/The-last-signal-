import os
import re

from database_manager import DatabaseManager


REPORT_PATH = os.environ.get(
    "REPORT",
    "reports/python-report.md"
)


def read_report():

    if not os.path.exists(REPORT_PATH):
        return ""

    with open(
        REPORT_PATH,
        encoding="utf-8"
    ) as file:

        return file.read()



def extract_float(
    pattern,
    text,
    default=0
):

    result = re.search(
        pattern,
        text
    )

    if result:
        return float(result.group(1))

    return default



def extract_int(
    pattern,
    text,
    default=0
):

    result = re.search(
        pattern,
        text
    )

    if result:
        return int(result.group(1))

    return default



def main():

    report = read_report()


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



    # Extraction des métriques

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


    bandit_high = extract_int(
        r"High severity issues:\s*(\d+)",
        report
    )


    bandit_medium = extract_int(
        r"Medium severity issues:\s*(\d+)",
        report
    )


    bandit_low = extract_int(
        r"Low severity issues:\s*(\d+)",
        report
    )


    failed_tests = extract_int(
        r"failed=(\d+)",
        report
    )


    passed_tests = extract_int(
        r"passed=(\d+)",
        report
    )



    db = DatabaseManager()


    run_id = db.add_run(

        run_number,

        branch,

        commit

    )


    db.add_quality(

        run_id,

        pylint,

        coverage,

        complexity

    )


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

        passed_tests + failed_tests,

        passed_tests,

        failed_tests,

        0,

        0

    ))



    db.cursor.execute(
    """

    INSERT INTO security

    (
        run_id,
        high,
        medium,
        low
    )

    VALUES (?,?,?,?)

    """,

    (

        run_id,

        bandit_high,

        bandit_medium,

        bandit_low

    ))


    db.connection.commit()


    db.close()


    print(
        "Database updated successfully"
    )



if __name__ == "__main__":

    main()