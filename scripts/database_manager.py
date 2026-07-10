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


        self.connection.commit()



    def add_run(
        self,
        run_number,
        branch,
        commit_hash,
        status="success"
    ):


        self.cursor.execute(
        """
        INSERT OR REPLACE INTO runs
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



    def close(self):

        self.connection.close()