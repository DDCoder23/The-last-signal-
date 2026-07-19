import os
import re

from .utils import (
    read_report,
    extract_int,
    extract_float,
)




REPORT_PATH = os.environ.get(
    "REPORT",
    "reports/rust/rust-report.md"
)


def update_rust_database(db):

    report = read_report(REPORT_PATH)

    if not report:
        print("Rust report not found.")
        return

    run_number = int(
        os.getenv("GITHUB_RUN_NUMBER", 0)
    )

    branch = os.getenv(
        "GITHUB_REF",
        "unknown"
    )

    commit = os.getenv(
        "GITHUB_SHA",
        "unknown"
    )



    run_id = db.add_run(
        run_number,
        branch,
        commit
    )

    # ==========================================
    # Résumé Rust
    # ==========================================

    clippy = extract_int(
        r"Clippy warnings:\s*(\d+)",
        report
    )

    fmt = extract_int(
        r"Rustfmt errors:\s*(\d+)",
        report
    )

    audit = extract_int(
        r"Cargo audit:\s*(\d+)",
        report
    )

    db.insert(
        "rust_summary",
        run_id=run_id,
        clippy=clippy,
        fmt=fmt,
        audit=audit
    )

    # ==========================================
    # Résumé des tests
    # ==========================================

    passed = extract_int(
        r"Passed tests:\s*(\d+)",
        report
    )

    failed = extract_int(
        r"Failed tests:\s*(\d+)",
        report
    )

    skipped = extract_int(
        r"Skipped tests:\s*(\d+)",
        report
    )

    duration = extract_float(
        r"Finished in ([0-9.]+)s",
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
    # Détails Clippy
    # ==========================================

    clippy_pattern = re.compile(
        r"--> (.*?):(\d+):\d+.*?\n.*?\n.*?warning: (.*)",
        re.S
    )

    for file, line, message in clippy_pattern.findall(report):

        db.insert(
            "clippy_warnings",
            run_id=run_id,
            file=file,
            line=int(line),
            level="warning",
            message=message.strip()
        )

    # ==========================================
    # Détails Cargo Audit
    # ==========================================

    audit_pattern = re.compile(
        r"Crate:\s*(.*?)\n.*?Version:\s*(.*?)\n.*?ID:\s*(.*?)\n",
        re.S
    )

    for package, version, advisory in audit_pattern.findall(report):

        db.insert(
            "cargo_audit",
            run_id=run_id,
            advisory=advisory.strip(),
            package=package.strip(),
            severity="unknown",
            version=version.strip()
        )

    db.close()

    print("Rust database updated successfully.")
