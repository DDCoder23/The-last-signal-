
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import tempfile
from enum import IntEnum
from pathlib import Path
from typing import Callable


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
# Résultats
# ============================================================

class IntegrityResult(IntEnum):
    """
    Résultats attendus du integrity_check.py.

    0 = intégrité OK
    1 = modification détectée
    2+ = erreur du checker
    """

    CLEAN = 0
    TAMPERING_DETECTED = 1
    CHECKER_ERROR = 2


# ============================================================
# Types
# ============================================================

Attack = Callable[[Path], None]


# ============================================================
# Exceptions
# ============================================================

class SecurityTestError(RuntimeError):
    """Erreur contrôlée du laboratoire de sécurité."""


# ============================================================
# Command execution
# ============================================================

def run(
    command: list[str],
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    Exécute une commande sans shell.

    IMPORTANT :
    shell=False est implicite et volontaire.
    """

    printable = " ".join(
        repr(part)
        for part in command
    )

    print(f"[CMD] {printable}")

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
        shell=False,
    )


# ============================================================
# SHA-256
# ============================================================

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ============================================================
# Validation environnement
# ============================================================

def validate_sha(value: str) -> bool:
    """
    Git SHA attendu : SHA-1 ou SHA-256 hexadécimal.
    """

    return bool(
        re.fullmatch(
            r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}",
            value,
        )
    )


def validate_repository_name(value: str) -> bool:
    """
    Format GitHub attendu :

        owner/repository
    """

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
            value,
        )
    )


def validate_github_server(value: str) -> bool:
    """
    Autorise uniquement une URL HTTP(S) simple,
    sans credentials ni chemin arbitraire.

    Exemples valides :
        https://github.com
        https://github.example.com
    """

    return bool(
        re.fullmatch(
            r"https://[A-Za-z0-9.-]+",
            value.rstrip("/"),
        )
    )


def validate_environment() -> None:
    print("\n=== ENVIRONMENT VALIDATION ===")

    if not REPOSITORY:
        raise SecurityTestError(
            "GITHUB_REPOSITORY is missing."
        )

    if not validate_repository_name(REPOSITORY):
        raise SecurityTestError(
            "Invalid GITHUB_REPOSITORY format."
        )

    if not SHA:
        raise SecurityTestError(
            "GITHUB_SHA is missing."
        )

    if not validate_sha(SHA):
        raise SecurityTestError(
            "GITHUB_SHA is not a valid SHA-1/SHA-256 value."
        )

    if not validate_github_server(GITHUB_SERVER):
        raise SecurityTestError(
            "GITHUB_SERVER_URL is invalid."
        )

    if not INTEGRITY_CHECKER.is_file():
        raise SecurityTestError(
            f"Integrity checker not found: "
            f"{INTEGRITY_CHECKER}"
        )

    print("[PASS] Environment validated.")


# ============================================================
# Git clone
# ============================================================

def clone_repository(
    destination: Path,
) -> None:

    repository_url = (
        f"{GITHUB_SERVER.rstrip('/')}/"
        f"{REPOSITORY}.git"
    )

    print(
        "\n=== CLONING TEST REPOSITORY ==="
    )

    print(
        f"Repository: {repository_url}"
    )

    print(
        f"Commit:     {SHA}"
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Clone
    # --------------------------------------------------------

    run(
        [
            "git",
            "-c",
            "protocol.version=2",
            "clone",
            "--no-tags",
            "--filter=blob:none",
            repository_url,
            str(destination),
        ]
    )

    # --------------------------------------------------------
    # Récupération du SHA exact
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Checkout détaché
    # --------------------------------------------------------

    run(
        [
            "git",
            "checkout",
            "--detach",
            SHA,
        ],
        cwd=destination,
    )

    # --------------------------------------------------------
    # Vérification HEAD
    # --------------------------------------------------------

    current_sha = run(
        [
            "git",
            "rev-parse",
            "HEAD",
        ],
        cwd=destination,
    ).stdout.strip()

    if current_sha.lower() != SHA.lower():
        raise SecurityTestError(
            "The clone does not correspond "
            "to the requested SHA.\n"
            f"Expected: {SHA}\n"
            f"Actual:   {current_sha}"
        )

    # --------------------------------------------------------
    # Vérification objet Git
    # --------------------------------------------------------

    object_type = run(
        [
            "git",
            "cat-file",
            "-t",
            "HEAD",
        ],
        cwd=destination,
    ).stdout.strip()

    if object_type != "commit":
        raise SecurityTestError(
            f"HEAD is not a commit: {object_type}"
        )

    print(
        f"[OK] Exact commit verified: "
        f"{current_sha}"
    )


# ============================================================
# Etat Git
# ============================================================

def git_status(
    repository: Path,
) -> str:

    result = run(
        [
            "git",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        cwd=repository,
        check=False,
    )

    if result.returncode != 0:
        raise SecurityTestError(
            "git status failed."
        )

    return result.stdout


def verify_git_clean(
    repository: Path,
) -> bool:

    print(
        "\n=== GIT STATE CHECK ==="
    )

    output = git_status(repository).strip()

    if output:
        print(
            "[FAIL] Repository is not clean:"
        )

        print(output)

        return False

    print(
        "[PASS] Git working tree is clean."
    )

    return True


# ============================================================
# Création du laboratoire
# ============================================================

def create_test_environment_files(
    repository: Path,
) -> None:

    print(
        "\n=== CREATING LABORATORY FILES ==="
    )

    # --------------------------------------------------------
    # Faux .env
    # --------------------------------------------------------

    env_file = repository / ".env"

    if not env_file.exists():

        env_file.write_text(
            (
                "# FAKE SECRET - TEST ONLY\n"
                "TEST_SECRET=FAKE_TEST_SECRET\n"
                "DATABASE_URL="
                "sqlite://security-test.db\n"
                "API_KEY=FAKE_API_KEY\n"
            ),
            encoding="utf-8",
        )

        print(
            "[LAB] Created fake .env"
        )

    # --------------------------------------------------------
    # Faux .idea
    # --------------------------------------------------------

    idea = repository / ".idea"

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
            """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="SecurityTest">
        <option name="test" value="original" />
    </component>
</project>
""",
            encoding="utf-8",
        )

        print(
            "[LAB] Created fake "
            ".idea/workspace.xml"
        )

    # --------------------------------------------------------
    # Faux vault
    # --------------------------------------------------------

    vault = (
        repository
        / "vault.enc"
    )

    if not vault.exists():

        vault.write_bytes(
            (
                b"FAKE_ENCRYPTED_VAULT_"
                b"SECURITY_TEST_ONLY"
            )
        )

        print(
            "[LAB] Created fake vault.enc"
        )


# ============================================================
# Recherche contrôlée de fichiers sensibles
# ============================================================

FORBIDDEN_FILENAMES = {
    "master.key",
    "id_rsa",
    "id_ed25519",
    "id_ecdsa",
    "id_dsa",
}

FORBIDDEN_SUFFIXES = {
    ".pem",
    ".p12",
    ".pfx",
    ".key",
}

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}


def is_ignored_path(
    path: Path,
    repository: Path,
) -> bool:

    try:
        relative = path.relative_to(
            repository
        )
    except ValueError:
        return True

    return bool(
        set(relative.parts)
        & IGNORED_DIRECTORIES
    )


def find_sensitive_files(
    repository: Path,
) -> list[Path]:

    found: list[Path] = []

    for path in repository.rglob("*"):

        if not path.is_file():
            continue

        if is_ignored_path(
            path,
            repository,
        ):
            continue

        if path.name in FORBIDDEN_FILENAMES:
            found.append(path)
            continue

        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            found.append(path)

    return found


# ============================================================
# Attaque master.key / secrets
# ============================================================

def attack_sensitive_file_discovery(
    repository: Path,
) -> bool:

    print(
        "\n[ATTACK] Searching for "
        "sensitive key material"
    )

    found = find_sensitive_files(
        repository
    )

    if not found:

        print(
            "[PASS] No forbidden key material found."
        )

        return True

    print(
        "[CRITICAL] Sensitive files found:"
    )

    for path in found:

        relative = path.relative_to(
            repository
        )

        print(
            f"  ! {relative}"
        )

    print(
        "[FAIL] Sensitive key material "
        "is exposed."
    )

    return False


# ============================================================
# Fichiers candidats
# ============================================================

def find_safe_file_candidates(
    repository: Path,
) -> list[Path]:

    candidates: list[Path] = []

    for path in repository.rglob("*"):

        if not path.is_file():
            continue

        if is_ignored_path(
            path,
            repository,
        ):
            continue

        if path.name in {
            ".security-baseline.json",
            "integrity_check.py",
            "attack_test.py",
        }:
            continue

        candidates.append(path)

    return sorted(candidates)


# ============================================================
# Attaque Cargo.lock
# ============================================================

def attack_cargo_lock(
    repository: Path,
) -> None:

    target = repository / "Cargo.lock"

    print(
        "\n[ATTACK] Cargo.lock"
    )

    if not target.exists():

        print(
            "[SKIP] Cargo.lock absent"
        )

        return

    original = target.read_bytes()

    target.write_bytes(
        original
        + b"\n# RED TEAM TEST\n"
    )

    print(
        "[ATTACK] Cargo.lock modified."
    )


# ============================================================
# Attaque .env
# ============================================================

def attack_env(
    repository: Path,
) -> None:

    target = repository / ".env"

    print(
        "\n[ATTACK] .env"
    )

    if not target.exists():
        raise SecurityTestError(
            ".env laboratory file absent."
        )

    content = target.read_text(
        encoding="utf-8"
    )

    content += (
        "\n"
        "ATTACK_TEST_MODIFICATION=TRUE\n"
    )

    target.write_text(
        content,
        encoding="utf-8",
    )

    print(
        "[ATTACK] .env modified."
    )


# ============================================================
# Attaque .idea
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
        raise SecurityTestError(
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
# Attaque création fichier
# ============================================================

def attack_file_creation(
    repository: Path,
) -> None:

    target = (
        repository
        / ".security-attack-created"
    )

    print(
        f"\n[ATTACK] Creating "
        f"{target.relative_to(repository)}"
    )

    target.write_text(
        "RED_TEAM_CREATION_TEST\n",
        encoding="utf-8",
    )

    print(
        "[ATTACK] New file created."
    )


# ============================================================
# Attaque suppression
# ============================================================

def attack_file_deletion(
    repository: Path,
) -> None:

    candidates = find_safe_file_candidates(
        repository
    )

    if not candidates:
        raise SecurityTestError(
            "No suitable file available "
            "for deletion attack."
        )

    target = candidates[0]

    print(
        f"\n[ATTACK] Deleting "
        f"{target.relative_to(repository)}"
    )

    target.unlink()

    print(
        "[ATTACK] File deleted."
    )


# ============================================================
# Attaque remplacement
# ============================================================

def attack_file_replacement(
    repository: Path,
) -> None:

    candidates = find_safe_file_candidates(
        repository
    )

    if not candidates:
        raise SecurityTestError(
            "No suitable file available "
            "for replacement attack."
        )

    target = candidates[0]

    print(
        f"\n[ATTACK] Replacing "
        f"{target.relative_to(repository)}"
    )

    target.write_bytes(
        b"RED_TEAM_REPLACEMENT_TEST\n"
    )

    print(
        "[ATTACK] File replaced."
    )


# ============================================================
# Accès security/
# ============================================================

def get_security_directory(
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


def attack_security_access(
    repository: Path,
) -> bool:

    security = get_security_directory(
        repository
    )

    print(
        "\n[ATTACK] Accessing security directory"
    )

    if security is None:

        print(
            "[SKIP] security directory absent."
        )

        return True

    accessed = 0

    for path in security.rglob("*"):

        if not path.is_file():
            continue

        try:

            path.stat()

            accessed += 1

            print(
                "[ACCESS] "
                f"{path.relative_to(repository)}"
            )

        except OSError as error:

            print(
                "[BLOCKED] "
                f"{path.relative_to(repository)}: "
                f"{error}"
            )

    print(
        f"[ATTACK] Files accessible: {accessed}"
    )

    print(
        "[PASS] Security directory access "
        "simulation completed."
    )

    return True


# ============================================================
# Modification security/
# ============================================================

def attack_security_file(
    repository: Path,
) -> None:

    security = get_security_directory(
        repository
    )

    print(
        "\n[ATTACK] Security directory tampering"
    )

    if security is None:

        print(
            "[SKIP] security directory absent."
        )

        return

    candidates = [
        path
        for path in security.rglob("*")
        if path.is_file()
        and path.name
        not in {
            "attack_test.py",
            "integrity_check.py",
        }
    ]

    if not candidates:

        print(
            "[SKIP] No suitable security file."
        )

        return

    target = sorted(candidates)[0]

    print(
        f"[TARGET] "
        f"{target.relative_to(repository)}"
    )

    original = target.read_bytes()

    target.write_bytes(
        original
        + b"\n# RED TEAM INTEGRITY TEST\n"
    )

    print(
        "[ATTACK] Security file modified."
    )


# ============================================================
# Corruption vault
# ============================================================

def attack_vault(
    repository: Path,
) -> None:

    target = repository / "vault.enc"

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
        raise SecurityTestError(
            "vault.enc is empty."
        )

    corrupted = bytearray(original)

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
# Restauration
# ============================================================

def restore_file(
    path: Path,
    original: bytes,
) -> bool:

    try:

        path.write_bytes(
            original
        )

        restored = path.read_bytes()

        return restored == original

    except OSError as error:

        print(
            "[CRITICAL] Restore failed "
            f"for {path}: {error}"
        )

        return False


# ============================================================
# Baseline
# ============================================================

def baseline_path(
    repository: Path,
) -> Path:

    return (
        repository
        / ".security-baseline.json"
    )


def create_baseline(
    repository: Path,
) -> None:

    run(
        [
            sys.executable,
            str(INTEGRITY_CHECKER),
            "create",
        ],
        cwd=repository,
    )


def remove_baseline(
    repository: Path,
) -> None:

    baseline_path(
        repository
    ).unlink(
        missing_ok=True
    )


# ============================================================
# Integrity checker
# ============================================================

def run_integrity_check(
    repository: Path,
) -> IntegrityResult:

    result = run(
        [
            sys.executable,
            str(INTEGRITY_CHECKER),
            "check",
        ],
        cwd=repository,
        check=False,
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode == 0:
        return IntegrityResult.CLEAN

    if result.returncode == 1:
        return IntegrityResult.TAMPERING_DETECTED

    print(
        "[CRITICAL] Integrity checker "
        f"returned unexpected code "
        f"{result.returncode}."
    )

    return IntegrityResult.CHECKER_ERROR


# ============================================================
# Vérification d'une attaque
# ============================================================

def execute_integrity_attack(
    name: str,
    repository: Path,
    attack: Attack,
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

    try:

        # ----------------------------------------------------
        # Baseline
        # ----------------------------------------------------

        create_baseline(
            repository
        )

        # ----------------------------------------------------
        # Vérification baseline
        # ----------------------------------------------------

        baseline_result = run_integrity_check(
            repository
        )

        if baseline_result != IntegrityResult.CLEAN:

            print(
                "[FAIL] Baseline is not clean."
            )

            return False

        # ----------------------------------------------------
        # Attaque
        # ----------------------------------------------------

        attack(
            repository
        )

        # ----------------------------------------------------
        # Détection
        # ----------------------------------------------------

        result = run_integrity_check(
            repository
        )

        if result == IntegrityResult.TAMPERING_DETECTED:

            print(
                "[PASS] Attack detected."
            )

            return True

        if result == IntegrityResult.CLEAN:

            print(
                "[FAIL] Attack was NOT detected."
            )

            return False

        print(
            "[FAIL] Integrity checker failed "
            "instead of reporting tampering."
        )

        return False

    except (OSError, subprocess.SubprocessError) as error:

        print(
            f"[ERROR] Attack execution failed: {error}"
        )

        return False

    finally:

        remove_baseline(
            repository
        )


# ============================================================
# Attaque vault avec restauration
# ============================================================

def execute_vault_attack(
    repository: Path,
) -> bool:

    print(
        "\n"
        + "=" * 70
    )

    print(
        " ATTACK: vault.enc corruption"
    )

    print(
        "=" * 70
    )

    vault = repository / "vault.enc"

    if not vault.exists():

        print(
            "[SKIP] vault.enc absent."
        )

        return True

    original = vault.read_bytes()

    try:

        # ----------------------------------------------------
        # Baseline
        # ----------------------------------------------------

        create_baseline(
            repository
        )

        baseline_result = run_integrity_check(
            repository
        )

        if baseline_result != IntegrityResult.CLEAN:

            print(
                "[FAIL] Vault baseline is not clean."
            )

            return False

        # ----------------------------------------------------
        # Attaque
        # ----------------------------------------------------

        attack_vault(
            repository
        )

        # ----------------------------------------------------
        # Détection
        # ----------------------------------------------------

        result = run_integrity_check(
            repository
        )

        if result != IntegrityResult.TAMPERING_DETECTED:

            print(
                "[FAIL] Vault corruption "
                "was not correctly detected."
            )

            return False

        print(
            "[PASS] Vault corruption detected."
        )

        return True

    except (OSError, subprocess.SubprocessError) as error:

        print(
            f"[ERROR] Vault attack failed: {error}"
        )

        return False

    finally:

        print(
            "[RESTORE] Restoring vault.enc..."
        )

        restored = restore_file(
            vault,
            original,
        )

        if not restored:

            print(
                "[CRITICAL] vault.enc "
                "restoration failed."
            )

        else:

            restored_hash = sha256_file(
                vault
            )

            original_hash = sha256_bytes(
                original
            )

            if restored_hash == original_hash:

                print(
                    "[RESTORE] vault.enc "
                    "restored exactly."
                )

            else:

                print(
                    "[CRITICAL] vault.enc "
                    "hash mismatch after restore."
                )

        remove_baseline(
            repository
        )


# ============================================================
# Suite d'attaques
# ============================================================

def run_attack_suite(
    repository: Path,
) -> list[tuple[str, bool]]:

    results: list[tuple[str, bool]] = []

    attacks: list[
        tuple[str, Attack]
    ] = [
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
        (
            "new file creation",
            attack_file_creation,
        ),
        (
            "file replacement",
            attack_file_replacement,
        ),
        (
            "file deletion",
            attack_file_deletion,
        ),
    ]

    for name, attack in attacks:

        result = execute_integrity_attack(
            name,
            repository,
            attack,
        )

        results.append(
            (
                name,
                result,
            )
        )

    # --------------------------------------------------------
    # security/
    # --------------------------------------------------------

    security = get_security_directory(
        repository
    )

    result = attack_security_access(
        repository
    )

    results.append(
        (
            "security access",
            result,
        )
    )

    if security is not None:

        result = execute_integrity_attack(
            "security directory tampering",
            repository,
            attack_security_file,
        )

        results.append(
            (
                "security tampering",
                result,
            )
        )

    # --------------------------------------------------------
    # vault
    # --------------------------------------------------------

    result = execute_vault_attack(
        repository
    )

    results.append(
        (
            "vault.enc",
            result,
        )
    )

    # --------------------------------------------------------
    # sensitive files
    # --------------------------------------------------------

    result = attack_sensitive_file_discovery(
        repository
    )

    results.append(
        (
            "sensitive key material exposure",
            result,
        )
    )

    return results


# ============================================================
# Résultats
# ============================================================

def print_results(
    results: list[tuple[str, bool]],
    git_ok: bool,
) -> int:

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
        "Git integrity: "
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


# ============================================================
# Main
# ============================================================

def main() -> int:

    print(
        "=" * 70
    )

    print(
        " THE LAST SIGNAL - "
        "RED TEAM FILE INTEGRITY TEST v2"
    )

    print(
        "=" * 70
    )

    try:

        # ----------------------------------------------------
        # Environnement
        # ----------------------------------------------------

        validate_environment()

        # ----------------------------------------------------
        # Laboratoire temporaire
        # ----------------------------------------------------

        with tempfile.TemporaryDirectory(
            prefix="the_last_signal_attack_"
        ) as temporary_directory:

            repository = (
                Path(temporary_directory)
                / "repository"
            )

            # -----------------------------------------------
            # Clone
            # -----------------------------------------------

            clone_repository(
                repository
            )

            # -----------------------------------------------
            # Vérification initiale
            # -----------------------------------------------

            if not verify_git_clean(
                repository
            ):

                print(
                    "[CRITICAL] "
                    "Fresh clone is not clean."
                )

                return 2

            # -----------------------------------------------
            # Laboratoire
            # -----------------------------------------------

            create_test_environment_files(
                repository
            )

            # -----------------------------------------------
            # Tests
            # -----------------------------------------------

            results = run_attack_suite(
                repository
            )

            # -----------------------------------------------
            # Vérification finale
            # -----------------------------------------------

            git_ok = verify_git_clean(
                repository
            )

            return print_results(
                results,
                git_ok,
            )

    except SecurityTestError as error:

        print(
            "\n[CRITICAL] Security test error:"
        )

        print(error)

        return 2

    except subprocess.CalledProcessError as error:

        print(
            "\n[CRITICAL] Command failed:"
        )

        print(
            f"Return code: {error.returncode}"
        )

        if error.stdout:
            print(error.stdout)

        return 2

    except KeyboardInterrupt:

        print(
            "\n[ABORTED] Test interrupted."
        )

        return 130

    except Exception as error:

        print(
            "\n[CRITICAL] Unexpected error:"
        )

        print(
            f"{type(error).__name__}: {error}"
        )

        return 2


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
```
