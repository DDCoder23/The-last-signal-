from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable


# ============================================================
# Configuration
# ============================================================

SCRIPT_DIRECTORY = Path(
    __file__
).resolve().parent

INTEGRITY_CHECKER = (
    SCRIPT_DIRECTORY
    / "integrity_check.py"
)

FAKE_ENV_CONTENT = (
    "# SECURITY LAB - FAKE SECRET ONLY\n"
    "TEST_SECRET=FAKE_TEST_SECRET\n"
    "DATABASE_URL=sqlite://security-test.db\n"
    "API_KEY=FAKE_API_KEY\n"
)

FAKE_WORKSPACE = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="SecurityTest">
        <option name="test" value="original" />
    </component>
</project>
"""

FAKE_VAULT = (
    b"FAKE_ENCRYPTED_VAULT_SECURITY_TEST_ONLY"
)


# ============================================================
# Command execution
# ============================================================

def run(
    command: list[str],
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:

    print(
        f"[CMD] {' '.join(command)}"
    )

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


# ============================================================
# SHA-256
# ============================================================

def sha256_bytes(
    content: bytes,
) -> str:

    return hashlib.sha256(
        content
    ).hexdigest()


def sha256_file(
    path: Path,
) -> str:

    digest = hashlib.sha256()

    with path.open("rb") as file:

        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# Arguments
# ============================================================

def parse_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "Red Team File Integrity Test"
        )
    )

    parser.add_argument(
        "--repository",
        required=True,
        type=Path,
        help=(
            "Path of the repository being tested."
        ),
    )

    parser.add_argument(
        "--baseline",
        required=True,
        type=Path,
        help=(
            "External baseline path."
        ),
    )

    return parser.parse_args()


# ============================================================
# Validation
# ============================================================

def validate_environment(
    repository: Path,
) -> None:

    if not repository.is_dir():

        raise RuntimeError(
            f"Repository does not exist: {repository}"
        )

    if not INTEGRITY_CHECKER.is_file():

        raise RuntimeError(
            "Integrity checker missing: "
            f"{INTEGRITY_CHECKER}"
        )


# ============================================================
# Laboratory files
# ============================================================

def create_test_environment_files(
    repository: Path,
) -> None:

    print(
        "\n=== CREATING SECURITY LABORATORY ==="
    )

    # --------------------------------------------------------
    # Fake .env
    # --------------------------------------------------------

    env_file = (
        repository
        / ".env"
    )

    if not env_file.exists():

        env_file.write_text(
            FAKE_ENV_CONTENT,
            encoding="utf-8",
        )

        print(
            "[LAB] Created fake .env"
        )

    # --------------------------------------------------------
    # Fake .idea
    # --------------------------------------------------------

    idea = (
        repository
        / ".idea"
    )

    idea.mkdir(
        parents=True,
        exist_ok=True,
    )

    workspace = (
        idea
        / "workspace.xml"
    )

    if not workspace.exists():

        workspace.write_text(
            FAKE_WORKSPACE,
            encoding="utf-8",
        )

        print(
            "[LAB] Created fake "
            ".idea/workspace.xml"
        )

    # --------------------------------------------------------
    # Fake vault
    # --------------------------------------------------------

    vault = (
        repository
        / "vault.enc"
    )

    if not vault.exists():

        vault.write_bytes(
            FAKE_VAULT
        )

        print(
            "[LAB] Created fake vault.enc"
        )


# ============================================================
# Integrity checker
# ============================================================

def create_baseline(
    repository: Path,
    baseline: Path,
) -> None:

    run(
        [
            sys.executable,
            str(INTEGRITY_CHECKER),
            "create",
            str(repository),
            str(baseline),
        ]
    )


def run_integrity_check(
    repository: Path,
    baseline: Path,
) -> bool:

    result = run(
        [
            sys.executable,
            str(INTEGRITY_CHECKER),
            "check",
            str(repository),
            str(baseline),
        ],
        check=False,
    )

    print(
        result.stdout
    )

    return result.returncode == 1


# ============================================================
# Attack helpers
# ============================================================

def append_bytes(
    path: Path,
    payload: bytes,
) -> None:

    original = path.read_bytes()

    path.write_bytes(
        original + payload
    )


def execute_integrity_attack(
    name: str,
    repository: Path,
    baseline: Path,
    attack: Callable[[Path], None],
) -> bool:

    print(
        "\n"
        + "=" * 70
    )

    print(
        f" ATTACK: {name}"
    )

    print(
        "=" * 70
    )

    create_baseline(
        repository,
        baseline,
    )

    try:

        attack(
            repository
        )

        detected = run_integrity_check(
            repository,
            baseline,
        )

        if not detected:

            print(
                "[FAIL] Attack was NOT detected."
            )

            return False

        print(
            "[PASS] Attack detected."
        )

        return True

    finally:

        baseline.unlink(
            missing_ok=True
        )


# ============================================================
# Cargo.lock attack
# ============================================================

def attack_cargo_lock(
    repository: Path,
) -> None:

    target = (
        repository
        / "Cargo.lock"
    )

    print(
        "\n[ATTACK] Cargo.lock"
    )

    if not target.exists():

        print(
            "[SKIP] Cargo.lock absent."
        )

        return

    append_bytes(
        target,
        b"\n# RED TEAM INTEGRITY TEST\n",
    )

    print(
        "[ATTACK] Cargo.lock modified."
    )


# ============================================================
# .env attack
# ============================================================

def attack_env(
    repository: Path,
) -> None:

    target = (
        repository
        / ".env"
    )

    print(
        "\n[ATTACK] .env"
    )

    if not target.exists():

        raise RuntimeError(
            ".env laboratory file missing."
        )

    append_bytes(
        target,
        b"\nATTACK_TEST_MODIFICATION=TRUE\n",
    )

    print(
        "[ATTACK] .env modified."
    )


# ============================================================
# .idea attack
# ============================================================

def attack_idea(
    repository: Path,
) -> None:

    target = (
        repository
        / ".idea"
        / "workspace.xml"
    )

    print(
        "\n[ATTACK] .idea/workspace.xml"
    )

    if not target.exists():

        raise RuntimeError(
            ".idea/workspace.xml missing."
        )

    content = target.read_text(
        encoding="utf-8"
    )

    if 'value="original"' not in content:

        raise RuntimeError(
            "Expected laboratory marker not found."
        )

    content = content.replace(
        'value="original"',
        'value="attacker-modified"',
        1,
    )

    target.write_text(
        content,
        encoding="utf-8",
    )

    print(
        "[ATTACK] .idea/workspace.xml modified."
    )


# ============================================================
# Security file attack
# ============================================================

def find_security_directory(
    repository: Path,
) -> Path | None:

    candidates = [
        repository / "security",
        repository / "tests" / "security",
    ]

    for directory in candidates:

        if directory.is_dir():
            return directory

    return None


def attack_security_file(
    repository: Path,
) -> None:

    security = find_security_directory(
        repository
    )

    print(
        "\n[ATTACK] Security directory tampering"
    )

    if security is None:

        print(
            "[SKIP] Security directory absent."
        )

        return

    candidates = []

    for path in security.rglob("*"):

        if not path.is_file():
            continue

        if path.name in {
            "attack_test.py",
            "integrity_check.py",
        }:
            continue

        if path.is_symlink():
            continue

        candidates.append(
            path
        )

    if not candidates:

        print(
            "[SKIP] No suitable security file."
        )

        return

    target = sorted(
        candidates
    )[0]

    print(
        f"[TARGET] "
        f"{target.relative_to(repository)}"
    )

    append_bytes(
        target,
        b"\n# RED TEAM INTEGRITY TEST\n",
    )

    print(
        "[ATTACK] Security file modified."
    )


# ============================================================
# Vault attack
# ============================================================

def attack_vault(
    repository: Path,
) -> None:

    target = (
        repository
        / "vault.enc"
    )

    print(
        "\n[ATTACK] vault.enc corruption"
    )

    if not target.exists():

        print(
            "[SKIP] vault.enc absent."
        )

        return

    original = target.read_bytes()

    if not original:

        raise RuntimeError(
            "vault.enc is empty."
        )

    corrupted = bytearray(
        original
    )

    positions = {
        0,
        len(corrupted) // 2,
        len(corrupted) - 1,
    }

    for position in positions:

        corrupted[position] ^= 0xFF

    target.write_bytes(
        bytes(corrupted)
    )

    print(
        "[ATTACK] vault.enc corrupted."
    )


# ============================================================
# master.key discovery
# ============================================================

def find_master_keys(
    repository: Path,
) -> list[Path]:

    found: list[Path] = []

    for path in repository.rglob(
        "master.key"
    ):

        try:

            relative = path.relative_to(
                repository
            )

        except ValueError:

            continue

        if ".git" in relative.parts:

            continue

        found.append(
            path
        )

    return found


def attack_master_key_discovery(
    repository: Path,
) -> bool:

    print(
        "\n[ATTACK] Searching for master.key"
    )

    found = find_master_keys(
        repository
    )

    if not found:

        print(
            "[PASS] master.key not present."
        )

        return True

    print(
        "[CRITICAL] master.key found!"
    )

    for path in found:

        print(
            f"  ! "
            f"{path.relative_to(repository)}"
        )

    print(
        "[FAIL] master.key is exposed."
    )

    return False


# ============================================================
# Git verification
# ============================================================

def verify_git_clean(
    repository: Path,
) -> bool:

    print(
        "\n=== GIT STATE CHECK ==="
    )

    result = run(
        [
            "git",
            "status",
            "--porcelain",
        ],
        cwd=repository,
        check=False,
    )

    if result.stdout.strip():

        print(
            result.stdout
        )

        print(
            "[INFO] Laboratory files or attack "
            "artifacts remain in the clone."
        )

    print(
        "[PASS] Git state inspection completed."
    )

    return True


# ============================================================
# Main
# ============================================================

def main() -> int:

    print(
        "=" * 70
    )

    print(
        " THE LAST SIGNAL - "
        "RED TEAM FILE INTEGRITY TEST v3"
    )

    print(
        "=" * 70
    )

    args = parse_arguments()

    repository = (
        args.repository
        .resolve()
    )

    baseline = (
        args.baseline
        .resolve()
    )

    try:

        validate_environment(
            repository
        )

        create_test_environment_files(
            repository
        )

    except (RuntimeError, OSError) as error:

        print(
            f"[ERROR] {error}"
        )

        return 2

    results: list[
        tuple[str, bool]
    ] = []

    # --------------------------------------------------------
    # Cargo.lock
    # --------------------------------------------------------

    try:

        result = execute_integrity_attack(
            "Cargo.lock tampering",
            repository,
            baseline,
            attack_cargo_lock,
        )

        results.append(
            ("Cargo.lock", result)
        )

    except Exception as error:

        print(
            f"[ERROR] Cargo.lock test: {error}"
        )

        results.append(
            ("Cargo.lock", False)
        )

    # --------------------------------------------------------
    # .env
    # --------------------------------------------------------

    try:

        result = execute_integrity_attack(
            ".env tampering",
            repository,
            baseline,
            attack_env,
        )

        results.append(
            (".env", result)
        )

    except Exception as error:

        print(
            f"[ERROR] .env test: {error}"
        )

        results.append(
            (".env", False)
        )

    # --------------------------------------------------------
    # .idea
    # --------------------------------------------------------

    try:

        result = execute_integrity_attack(
            ".idea tampering",
            repository,
            baseline,
            attack_idea,
        )

        results.append(
            (".idea", result)
        )

    except Exception as error:

        print(
            f"[ERROR] .idea test: {error}"
        )

        results.append(
            (".idea", False)
        )

    # --------------------------------------------------------
    # Security directory
    # --------------------------------------------------------

    if find_security_directory(
        repository
    ) is not None:

        try:

            result = execute_integrity_attack(
                "security directory tampering",
                repository,
                baseline,
                attack_security_file,
            )

            results.append(
                ("security tampering", result)
            )

        except Exception as error:

            print(
                f"[ERROR] Security test: {error}"
            )

            results.append(
                ("security tampering", False)
            )

    else:

        print(
            "[SKIP] No security directory."
        )

    # --------------------------------------------------------
    # vault.enc
    # --------------------------------------------------------

    if (
        repository
        / "vault.enc"
    ).exists():

        try:

            result = execute_integrity_attack(
                "vault.enc corruption",
                repository,
                baseline,
                attack_vault,
            )

            results.append(
                ("vault.enc", result)
            )

        except Exception as error:

            print(
                f"[ERROR] vault.enc test: {error}"
            )

            results.append(
                ("vault.enc", False)
            )

    else:

        print(
            "[SKIP] vault.enc absent."
        )

    # --------------------------------------------------------
    # master.key
    # --------------------------------------------------------

    results.append(
        (
            "master.key exposure",
            attack_master_key_discovery(
                repository
            ),
        )
    )

    # --------------------------------------------------------
    # Git
    # --------------------------------------------------------

    git_ok = verify_git_clean(
        repository
    )

    # ========================================================
    # Result
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        " FINAL RED TEAM RESULT"
    )

    print(
        "=" * 70
    )

    passed = 0

    for name, result in results:

        status = (
            "PASS"
            if result
            else "FAIL"
        )

        print(
            f"{status:>5} | {name}"
        )

        if result:
            passed += 1

    total = len(results)

    print(
        "\n"
        f"Security scenarios: "
        f"{passed}/{total}"
    )

    print(
        "Git inspection: "
        f"{'PASS' if git_ok else 'FAIL'}"
    )

    if (
        passed == total
        and git_ok
    ):

        print(
            "\n[PASS] "
            "RED TEAM TEST PASSED."
        )

        return 0

    print(
        "\n[FAIL] "
        "RED TEAM TEST FAILED."
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
