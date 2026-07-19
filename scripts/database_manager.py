import os
import sqlite3
from datetime import datetime


DB_PATH = "database/ci_reports.db"


class DatabaseManager:

    def __init__(self, db_path=DB_PATH):

        os.makedirs("database", exist_ok=True)

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.create_tables()

    # =====================================================
    # TABLES
    # =====================================================

    def create_tables(self):

        self.cursor.executescript("""

        ----------------------------------------------------
        -- RUNS
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS runs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_number INTEGER UNIQUE,

            workflow TEXT,

            branch TEXT,

            commit_hash TEXT,

            date TEXT,

            status TEXT
        );

        ----------------------------------------------------
        -- QUALITY
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS quality_metrics (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            pylint REAL,

            coverage REAL,

            complexity REAL,

            documentation REAL,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- TEST SUMMARY
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS test_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            total INTEGER,

            passed INTEGER,

            failed INTEGER,

            skipped INTEGER,

            duration REAL,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- SECURITY SUMMARY
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS security_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            total INTEGER,

            high INTEGER,

            medium INTEGER,

            low INTEGER,

            affected_files INTEGER,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- DOCUMENTATION SUMMARY
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS documentation_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            score REAL,

            errors INTEGER,

            warnings INTEGER,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- RUST SUMMARY
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS rust_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            clippy INTEGER,

            fmt INTEGER,

            audit INTEGER,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- FLAKE8
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS flake8_errors (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            file TEXT,

            line INTEGER,

            column_number INTEGER,

            code TEXT,

            message TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- BLACK
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS black_files (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            file TEXT,

            status TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- BANDIT
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS bandit_issues (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            test TEXT,

            severity TEXT,

            confidence TEXT,

            cwe TEXT,

            info TEXT,

            file TEXT,

            line INTEGER,

            column_number INTEGER,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- PYTEST
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS pytest_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            test_name TEXT,

            status TEXT,

            duration REAL,

            error TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- DOC PROBLEMS
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS doc_problems (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            file TEXT,

            severity TEXT,

            module TEXT,

            message TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- CLIPPY
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS clippy_warnings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            file TEXT,

            line INTEGER,

            level TEXT,

            message TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- CARGO AUDIT
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS cargo_audit (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            advisory TEXT,

            package TEXT,

            severity TEXT,

            version TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        ----------------------------------------------------
        -- REPORTS
        ----------------------------------------------------

        CREATE TABLE IF NOT EXISTS reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id INTEGER,

            report_type TEXT,

            markdown TEXT,

            FOREIGN KEY(run_id) REFERENCES runs(id)
        );

        """)

        self.connection.commit()

    # =====================================================
    # RUN
    # =====================================================

    def add_run(
        self,
        run_number,
        branch,
        commit_hash,
        workflow="CI",
        status="success"
    ):

        self.cursor.execute(
            """
            SELECT id
            FROM runs
            WHERE run_number=?
            """,
            (run_number,)
        )

        row = self.cursor.fetchone()

        if row:
            return row["id"]

        self.cursor.execute(
            """
            INSERT INTO runs
            (
                run_number,
                workflow,
                branch,
                commit_hash,
                date,
                status
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                run_number,
                workflow,
                branch,
                commit_hash,
                datetime.utcnow().isoformat(),
                status
            )
        )

        self.connection.commit()

        return self.cursor.lastrowid

    # =====================================================
    # INSERT GENERIQUE
    # =====================================================

    def insert(self, table, **values):

        columns = ", ".join(values.keys())
        placeholders = ", ".join("?" for _ in values)

        self.cursor.execute(
            f"""
            INSERT INTO {table}
            ({columns})
            VALUES ({placeholders})
            """,
            tuple(values.values())
        )

        self.connection.commit()

        return self.cursor.lastrowid

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):
        self.connection.close()
    def add_security(self,run_id,high,medium,low,total,files):
        self.cursor.execute(
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
            files,
        ),
    )
        self.connection.commit()
    def add_security_issue(self,run_id,test,severity,confidence,cwe,info,file,line,column):
        self.cursor.execute(
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
            test,
            severity,
            confidence,
            cwe,
            info,
            file,
            line,
            column,
        ),
    )
        self.connection.commit()
    
