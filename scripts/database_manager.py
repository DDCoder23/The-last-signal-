import sqlite3
import os
from datetime import datetime


DB_PATH = "database/python_reports.db"


class DatabaseManager:

    def __init__(self, db_path=DB_PATH):

        os.makedirs(
            "database",
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            db_path
        )

        self.cursor = self.connection.cursor()

        self.create_tables()


    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_number INTEGER UNIQUE,

            date TEXT,

            branch TEXT,

            commit_hash TEXT,

            status TEXT

        )
        """)


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_metrics (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            pylint REAL,

            coverage REAL,

            complexity REAL,

            documentation REAL,

            FOREIGN KEY(run_id)
            REFERENCES runs(id)

        )
        """)


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            total INTEGER,

            passed INTEGER,

            failed INTEGER,

            skipped INTEGER,

            duration REAL,

            FOREIGN KEY(run_id)
            REFERENCES runs(id)

        )
        """)


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS security (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            high INTEGER,

            medium INTEGER,

            low INTEGER,

            FOREIGN KEY(run_id)
            REFERENCES runs(id)

        )
        """)
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS flake8_errors (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_id INTEGER,

    file TEXT,

    line INTEGER,

    column_number INTEGER,

    code TEXT,

    message TEXT,

    FOREIGN KEY(run_id)
    REFERENCES runs(id)

)
""")
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS black_files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_id INTEGER,

    file TEXT,

    status TEXT,

    FOREIGN KEY(run_id)
    REFERENCES runs(id)

)
""")
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS bandit_issues (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_id INTEGER,

    severity TEXT,

    confidence TEXT,

    file TEXT,

    line INTEGER,

    issue TEXT,

    FOREIGN KEY(run_id)
    REFERENCES runs(id)

)
""")
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS pytest_results (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_id INTEGER,

    test_name TEXT,

    status TEXT,

    duration REAL,

    error TEXT,

    FOREIGN KEY(run_id)
    REFERENCES runs(id)

)
""")
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_id INTEGER,

    markdown TEXT,

    FOREIGN KEY(run_id)
    REFERENCES runs(id)

)
""")
        self.connection.commit()



    def add_run(
        self,
        run_number,
        branch,
        commit_hash,
        status="success"
    ):

        try:
            self.cursor.execute(
        """
        INSERT INTO runs
        (
            run_number,
            date,
            branch,
            commit_hash,
            status
        )

        VALUES (?,?,?,?,?)

        """,

        (

            run_number,

            str(datetime.now()),

            branch,

            commit_hash,

            status

        ))
            self.connection.commit()
            return self.cursor.lastrowid

        except Exception:
            self.cursor.execute(
            """
            SELECT id
            FROM runs
            WHERE run_number=?
            """,
            (run_number,)
        )
            return self.cursor.fetchone()[0]



    def add_quality(
        self,
        run_id,
        pylint,
        coverage,
        complexity,
        documentation=0
    ):


        self.cursor.execute(
        """

        INSERT INTO quality_metrics

        (
        run_id,
        pylint,
        coverage,
        complexity,
        documentation
        )

        VALUES (?,?,?,?,?)

        """,

        (
            run_id,
            pylint,
            coverage,
            complexity,
            documentation
        ))


        self.connection.commit()


    def add_flake8_error(self,run_id,file,line,column,code,message):

        self.cursor.execute(
        """
        INSERT INTO flake8_errors
        (
            run_id,
            file,
            line,
            column_number,
            code,
            message
        )

        VALUES (?,?,?,?,?,?)
        """,
        (
            run_id,
            file,
            line,
            column,
            code,
            message
        )
    )

        self.connection.commit()

    def add_black_file(self,run_id,file,status):

        self.cursor.execute(
        """
        INSERT INTO black_file
        (
            run_id,
            file,
            status
        )

        VALUES (?,?,?)
        """,
        (
            run_id,
            file,
            status
        )
    )

        self.connection.commit()


    def add_bandit_issue(self,run_id,file,status):

        self.cursor.execute(
        """
        INSERT INTO bandit_issue
        (
            run_id,
            file,
            status
        )

        VALUES (?,?,?)
        """,
        (
            run_id,
            file,
            status
        )
    )

        self.connection.commit()
    def add_test(self,run_id,file,status):

        self.cursor.execute(
        """
        INSERT INTO test
        (
            run_id,
            file,
            status
        )

        VALUES (?,?,?)
        """,
        (
            run_id,
            file,
            status
        )
    )

        self.connection.commit()
    def close(self):

        self.connection.close()
