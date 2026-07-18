import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path
from update_database import update_database

DB_PATH = Path("database/python_reports.db")
DOC_SCORE_PATH = Path("reports/docs/score.json")
OUTPUT = "dashboard/data/dashboard.json"

def get_documentation_score():

    if not os.path.exists(DOC_SCORE_PATH):
        return {
            "score": 0,
            "details": {}
        }


    with open(
        DOC_SCORE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
def get_database_data():

    if not os.path.exists(DB_PATH):
        print("Base SQLite introuvable")
        return []


    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()


    cursor.execute("""
    SELECT

        runs.id,
        runs.run_number,
        runs.date,
        runs.branch,
        runs.commit_hash,
        runs.status,

        quality_metrics.pylint,
        quality_metrics.coverage,
        quality_metrics.complexity,
        quality_metrics.documentation,

        tests.total,
        tests.passed,
        tests.failed,
        tests.skipped,
        tests.duration,

        security.high,
        security.medium,
        security.low


    FROM runs


    LEFT JOIN quality_metrics

    ON runs.id = quality_metrics.run_id


    LEFT JOIN tests

    ON runs.id = tests.run_id


    LEFT JOIN security

    ON runs.id = security.run_id


    ORDER BY runs.id ASC

    """)


    data = cursor.fetchall()

    connection.close()


    return data



def calculate_quality(
        coverage,
        pylint,
        documentation,
        security
):

    coverage = coverage or 0
    pylint = pylint or 0
    documentation = documentation or 0


    security_score = max(
        0,
        100 - security * 10
    )


    score = (

        coverage * 0.4 +

        (pylint * 10) * 0.3 +

        documentation * 0.2 +

        security_score * 0.1

    )


    return round(score,2)



def generate_json(rows):

    docu=get_documentation_score()
    os.makedirs(
        "dashboard/data",
        exist_ok=True
    )
    

    dashboard = {

        "generated": str(datetime.now()),
        

        "summary": {

            "total_runs": len(rows),

            "average_quality": 0,

            "average_coverage": 0,

            "average_pylint": 0,

            "security_errors": 0

        },


        "history": []

    }


    total_quality = 0
    total_coverage = 0
    total_pylint = 0
    total_security = 0



    for row in rows:


        (
            id,
            run,
            date,
            branch,
            commit,
            status,

            pylint,
            coverage,
            complexity,
            documentation,

            tests_total,
            tests_passed,
            tests_failed,
            tests_skipped,
            duration,

            high,
            medium,
            low

        ) = row



        security_errors = (

            (high or 0)
            +
            (medium or 0)
            +
            (low or 0)

        )
        doc_score = docu.get(
    "score",
    0
)


        quality = calculate_quality(

            coverage,

            pylint,

             doc_score,

            security_errors

        )



        total_quality += quality

        total_coverage += coverage or 0

        total_pylint += pylint or 0

        total_security += security_errors



        dashboard["history"].append({

            "run": run,

            "date": date,

            "branch": branch,

            "commit": commit,

            "status": status,


            "quality": quality,


            "coverage": coverage or 0,

            "pylint": pylint or 0,

            "complexity": complexity or 0,


            "tests": {

                "total": tests_total or 0,

                "passed": tests_passed or 0,

                "failed": tests_failed or 0,

                "skipped": tests_skipped or 0,

                "duration": duration or 0

            },


            "security": {

                "high": high or 0,

                "medium": medium or 0,

                "low": low or 0

            },
            "documentation": {

    "score": doc_score,

    "details":
        docu.get(
            "details",
            {}
        )

},

        })



    if rows:


        dashboard["summary"]["average_quality"] = round(
            total_quality / len(rows),
            2
        )


        dashboard["summary"]["average_coverage"] = round(
            total_coverage / len(rows),
            2
        )


        dashboard["summary"]["average_pylint"] = round(
            total_pylint / len(rows),
            2
        )


        dashboard["summary"]["security_errors"] = total_security



    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            dashboard,
            file,
            indent=4,
            ensure_ascii=False
        )



    print(
        "Dashboard JSON généré :",
        OUTPUT
    )



if __name__ == "__main__":
    update_database()
    
    rows = get_database_data()

    generate_json(rows)
