from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

REPOSITORY = os.environ.get(
    "GITHUB_REPOSITORY",
    "",
)

SHA = os.environ.get(
    "GITHUB_SHA",
    "",
)

GITHUB_SERVER = os.environ.get(
    "GITHUB_SERVER_URL",
    "https://github.com",
)

INTEGRITY_CHECKER = (
    Path(__file__).resolve().parent
    / "integrity_check.py"
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
# Git clone
# ============================================================

def clone_repository(destination: Path) -> None:
    if not REPOSITORY:
        raise RuntimeError(
            "GITHUB_REPOSITORY n'est pas défini."
        )

    if not SHA:
        raise RuntimeError(
            "GITHUB_SHA n'est pas défini."
        )

    repository_url = (
        f"{GITHUB_SERVER}/{REPOSITORY}.git"
    )

    print("\n=== CLONING TEST REPOSITORY ===")
    print(f"Repository: {repository_url}")
    print(f"Commit:     {SHA}")

    run(
        [
            "git",
            "clone",
            "--no-tags",
            "--depth",
            "1",
            repository_url,
            str(destination),
        ]
    )

    # On s'assure que le clone correspond exactement
    # au commit testé par GitHub Actions.
    run(
        [
            "git",
            "fetch",
            "--depth",
            "1",
            "origin",
            SHA,
        ],
        cwd=destination,
    )

    run(
        [
            "git",
            "checkout",
            "--detach",
            SHA,
        ],
        cwd=destination,
    )

    current_sha = run(
        [
            "git",
            "rev-parse",
            "HEAD",
        ],
        cwd=destination,
    ).stdout.strip()

    if current_sha != SHA:
        raise RuntimeError(
            "Le clone ne correspond pas au SHA du workflow.\n"
            f"Expected: {SHA}\n"
            f"Actual:   {current_sha}"
        )

    print(
        f"[OK] Exact commit verified: {current_sha}"
    )


# ============================================================
# Faux fichiers sensibles
# ============================================================

def create_test_environment_files(
    repository: Path,
) -> None:

    # --------------------------------------------------------
    # .env
    # --------------------------------------------------------

    env_file = repository / ".env"

    if not env_file.exists():
        env_file.write_text(
            """
# FAKE SECRET - SECURITY TEST ONLY
TEST_SECRET=FAKE_TEST_SECRET
DATABASE_URL=sqlite://security-test.db
API_KEY=FAKE_API_KEY
""".lstrip(),
            encoding="utf-8",
        )

        print("[LAB] Created fake .env")

    # --------------------------------------------------------
    # .idea
    # --------------------------------------------------------

    idea = repository / ".idea"
    idea.mkdir(exist_ok=True)

    workspace = idea / "workspace.xml"

    if not workspace.exists():
        workspace.write_text(
            """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="SecurityTest">
        <option name="test" value="original" />
    </component>
</project>
""",
            encoding="utf-8",
        )

        print("[LAB] Created fake .idea/workspace.xml")


# ============================================================
# Attaques
# ============================================================

def attack_cargo_lock(repository: Path) -> None:
    target = repository / "Cargo.lock"

    print("\n[ATTACK] Cargo.lock")

    if not target.exists():
        print("[SKIP] Cargo.lock absent")
        return

    content = target.read_text(
        encoding="utf-8"
    )

    marker = "\n# SECURITY RED TEAM TEST\n"

    target.write_text(
        content + marker,
        encoding="utf-8",
    )

    print(
        "[ATTACK] Cargo.lock modified."
    )


def attack_env(repository: Path) -> None:
    target = repository / ".env"

    print("\n[ATTACK] .env")

    if not target.exists():
        raise RuntimeError(
            ".env de laboratoire absent."
        )

    content = target.read_text(
        encoding="utf-8"
    )

    content += (
        "\nATTACK_TEST_MODIFICATION=TRUE\n"
    )

    target.write_text(
        content,
        encoding="utf-8",
    )

    print(
        "[ATTACK] .env modified."
    )


def attack_idea(repository: Path) -> None:
    target = (
        repository
        / ".idea"
        / "workspace.xml"
    )

    print("\n[ATTACK] .idea/workspace.xml")

    if not target.exists():
        raise RuntimeError(
            ".idea/workspace.xml absent."
        )

    content = target.read_text(
        encoding="utf-8"
    )

    content = content.replace(
        'value="original"',
        'value="attacker-modified"',
    )

    target.write_text(
        content,
        encoding="utf-8",
    )

    print(
        "[ATTACK] .idea/workspace.xml modified."
    )


# ============================================================
# Exécution d'une attaque
# ============================================================

def execute_attack(
    name: str,
    repository: Path,
    attack,
) -> bool:

    print("\n" + "=" * 70)
    print(f" ATTACK: {name}")
    print("=" * 70)

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    run(
        [
            sys.executable,
            str(INTEGRITY_CHECKER),
            "create",
        ],
        cwd=repository,
    )

    try:
        # ----------------------------------------------------
        # Attaque
        # ----------------------------------------------------

        attack(repository)

        # ----------------------------------------------------
        # Défense
        # ----------------------------------------------------

        result = run(
            [
                sys.executable,
                str(INTEGRITY_CHECKER),
                "check",
            ],
            cwd=repository,
            check=False,
        )

        output = result.stdout

        print(output)

        # ----------------------------------------------------
        # Une attaque réussie doit être détectée.
        # ----------------------------------------------------

        if result.returncode != 1:
            print(
                "[FAIL] Attack was NOT detected."
            )

            return False

        print(
            "[PASS] Attack detected."
        )

        return True

    finally:
        # ----------------------------------------------------
        # Suppression de la baseline
        # ----------------------------------------------------

        baseline = (
            repository
            / ".security-baseline.json"
        )

        baseline.unlink(
            missing_ok=True
        )


# ============================================================
# Vérification de sécurité du clone
# ============================================================

def verify_git_clean(repository: Path) -> bool:
    print("\n=== GIT STATE CHECK ===")

    result = run(
        [
            "git",
            "status",
            "--porcelain",
        ],
        cwd=repository,
        check=False,
    )

    print(result.stdout)

    # Le clone peut contenir les fichiers de laboratoire
    # (.env / .idea). Ils ne doivent jamais être commités.
    #
    # On vérifie surtout qu'aucune modification Git n'a été
    # faite dans les fichiers suivis par le dépôt.

    tracked_changes = run(
        [
            "git",
            "diff",
            "--exit-code",
        ],
        cwd=repository,
        check=False,
    )

    if tracked_changes.returncode != 0:
        print(
            "[FAIL] Tracked repository files were modified."
        )
        return False

    print(
        "[PASS] No tracked source modification remains."
    )

    return True


# ============================================================
# Main
# ============================================================

def main() -> int:

    print("=" * 70)
    print(" THE LAST SIGNAL - RED TEAM FILE INTEGRITY TEST")
    print("=" * 70)

    if not REPOSITORY:
        print(
            "[ERROR] GITHUB_REPOSITORY is missing."
        )
        return 2

    if not SHA:
        print(
            "[ERROR] GITHUB_SHA is missing."
        )
        return 2

    if not INTEGRITY_CHECKER.exists():
        print(
            f"[ERROR] Integrity checker not found:\n"
            f"{INTEGRITY_CHECKER}"
        )
        return 2

    attacks = [
        (
            "Cargo.lock tampering",
            attack_cargo_lock,
        ),
        (
            ".env tampering",
            attack_env,
        ),
        (
            ".idea tampering",
            attack_idea,
        ),
    ]

    results: list[bool] = []

    # ========================================================
    # Temporary laboratory
    # ========================================================

    with tempfile.TemporaryDirectory(
        prefix="the_last_signal_attack_"
    ) as temporary_directory:

        laboratory = (
            Path(temporary_directory)
            / "repository"
        )

        # ----------------------------------------------------
        # Clone
        # ----------------------------------------------------

        clone_repository(laboratory)

        # ----------------------------------------------------
        # Laboratory-only files
        # ----------------------------------------------------

        create_test_environment_files(
            laboratory
        )

        # ----------------------------------------------------
        # Attacks
        # ----------------------------------------------------

        for name, attack in attacks:

            result = execute_attack(
                name,
                laboratory,
                attack,
            )

            results.append(result)

        # ----------------------------------------------------
        # Final Git check
        # ----------------------------------------------------

        git_ok = verify_git_clean(
            laboratory
        )

    # ========================================================
    # Final result
    # ========================================================

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 70)
    print(" FINAL RESULT")
    print("=" * 70)

    print(
        f"Attacks detected : {passed}/{total}"
    )

    print(
        f"Git integrity    : "
        f"{'PASS' if git_ok else 'FAIL'}"
    )

    if passed == total and git_ok:
        print(
            "\n[PASS] RED TEAM TEST PASSED."
        )
        return 0

    print(
        "\n[FAIL] RED TEAM TEST FAILED."
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
