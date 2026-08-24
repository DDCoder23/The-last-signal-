from __future__ import annotations
import pytest
import os
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
# SHA-256
# ============================================================

def sha256_file(path: Path) -> str:

    import hashlib

    digest = hashlib.sha256()

    with path.open("rb") as file:

        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# Git clone
# ============================================================

def clone_repository(
    destination: Path,
) -> None:

    if not REPOSITORY:

        raise RuntimeError(
            "GITHUB_REPOSITORY n'est pas défini."
        )

    if not SHA:

        raise RuntimeError(
            "GITHUB_SHA n'est pas défini."
        )

    repository_url = (
        f"{GITHUB_SERVER}/"
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

    # --------------------------------------------------------
    # Clone
    # --------------------------------------------------------

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
    # Vérification
    # --------------------------------------------------------

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
            "Le clone ne correspond pas "
            "au SHA du workflow.\n"
            f"Expected: {SHA}\n"
            f"Actual:   {current_sha}"
        )

    print(
        f"[OK] Exact commit verified: "
        f"{current_sha}"
    )


# ============================================================
# Création du laboratoire
# ============================================================

def create_test_environment_files(
    repository: Path,
) -> None:

    print(
        "\n=== CREATING LABORATORY FILES ==="
    )

    # ========================================================
    # Faux .env
    # ========================================================

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

    # ========================================================
    # Faux .idea
    # ========================================================

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

    # ========================================================
    # Faux vault si absent
    # ========================================================

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
# Recherche contrôlée de master.key
# ============================================================

def find_master_keys(
    repository: Path,
) -> list[Path]:

    print(
        "\n[ATTACK] Searching for master.key"
    )

    found: list[Path] = []

    for path in repository.rglob("master.key"):

        # Ne jamais entrer dans .git.
        try:
            relative = path.relative_to(
                repository
            )
        except ValueError:
            continue

        if ".git" in relative.parts:
            continue

        found.append(path)

    return found


def attack_master_key_discovery(
    repository: Path,
) -> bool:

    """
    Cherche uniquement l'existence de master.key.

    IMPORTANT :
    Le contenu du fichier n'est jamais lu.
    """

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

        relative = path.relative_to(
            repository
        )

        print(
            f"  ! {relative}"
        )

    print(
        "[FAIL] A master.key is exposed "
        "inside the repository."
    )

    return False


# ============================================================
# Attaque Cargo.lock
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
            "[SKIP] Cargo.lock absent"
        )

        return

    original = target.read_bytes()

    # Modification contrôlée.
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

    target = (
        repository
        / ".env"
    )

    print(
        "\n[ATTACK] .env"
    )

    if not target.exists():

        raise RuntimeError(
            ".env de laboratoire absent."
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
# Scénario : accès au dossier security
# ============================================================

def attack_security_access(
    repository: Path,
) -> bool:

    security = (
        repository
        / "security"
    )

    # Le projet peut avoir tests/security
    # plutôt que security/.
    if not security.exists():

        security = (
            repository
            / "tests"
            / "security"
        )

    print(
        "\n[ATTACK] Accessing security directory"
    )

    if not security.exists():

        print(
            "[SKIP] security directory absent."
        )

        return True

    accessed = 0

    # --------------------------------------------------------
    # Parcours récursif.
    #
    # Nous ne lisons pas le contenu des secrets.
    # Nous vérifions seulement que les fichiers sont
    # accessibles dans le laboratoire.
    # --------------------------------------------------------

    for path in security.rglob("*"):

        if not path.is_file():
            continue

        try:
            path.stat()

            accessed += 1

            print(
                f"[ACCESS] "
                f"{path.relative_to(repository)}"
            )

        except OSError as error:

            print(
                f"[BLOCKED] "
                f"{path.relative_to(repository)}: "
                f"{error}"
            )

    print(
        f"[ATTACK] Files accessible: {accessed}"
    )

    # L'accès à un répertoire du clone est volontaire.
    # Le vrai test d'intégrité sera celui de la modification.
    print(
        "[PASS] Security directory access "
        "simulation completed."
    )

    return True


# ============================================================
# Scénario : modification security/
# ============================================================

def attack_security_file(
    repository: Path,
) -> Path | None:

    security = (
        repository
        / "security"
    )

    if not security.exists():

        security = (
            repository
            / "tests"
            / "security"
        )

    print(
        "\n[ATTACK] Security directory tampering"
    )

    if not security.exists():

        print(
            "[SKIP] security directory absent."
        )

        return None

    candidates = [
        path
        for path in security.rglob("*")
        if path.is_file()
        and path.name
        != "attack_test.py"
        and path.name
        != "integrity_check.py"
    ]

    if not candidates:

        print(
            "[SKIP] No suitable security file."
        )

        return None

    target = candidates[0]

    print(
        f"[TARGET] "
        f"{target.relative_to(repository)}"
    )

    # --------------------------------------------------------
    # Modification contrôlée.
    #
    # On ajoute une marque de test.
    # --------------------------------------------------------

    original = target.read_bytes()

    target.write_bytes(
        original
        + b"\n# RED TEAM INTEGRITY TEST\n"
    )

    print(
        "[ATTACK] Security file modified."
    )

    return target


# ============================================================
# Scénario : corruption de vault.enc
# ============================================================
def attack_vault(repository: Path) -> tuple[bool, bytes | None]:

    target = repository / "vault.enc"

    print("\n[ATTACK] vault.enc corruption")

    if not target.exists():
        print("[SKIP] vault.enc absent.")
        return True, None

    original = target.read_bytes()

    if not original:
        print("[FAIL] vault.enc is empty.")
        return False, original

    corrupted = bytearray(original)

    positions = {
        0,
        len(corrupted) // 2,
        len(corrupted) - 1,
    }

    for position in positions:
        corrupted[position] ^= 0xFF

    target.write_bytes(bytes(corrupted))

    print("[ATTACK] vault.enc corrupted.")

    return True, original


  
       
    

   

    

# ============================================================
# Restauration d'un fichier
# ============================================================

def restore_file(
    path: Path,
    original: bytes,
) -> bool:

    try:

        path.write_bytes(
            original
        )

        return (
            path.read_bytes()
            == original
        )

    except OSError as error:

        print(
            f"[CRITICAL] Restore failed "
            f"for {path}: {error}"
        )

        return False


# ============================================================
# Scanner après attaque
# ============================================================

def run_integrity_check(
    repository: Path,
) -> bool:

    result = run(
        [
            sys.executable,
            str(INTEGRITY_CHECKER),
            "check",
        ],
        cwd=repository,
        check=False,
    )

    print(
        result.stdout
    )

    return result.returncode == 1


# ============================================================
# Scénario d'attaque avec intégrité
# ============================================================

def execute_integrity_attack(
    name: str,
    repository: Path,
    attack,
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
        # Détection
        # ----------------------------------------------------

        detected = run_integrity_check(
            repository
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

        baseline = (
            repository
            / ".security-baseline.json"
        )

        baseline.unlink(
            missing_ok=True
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

    vault = (
        repository
        / "vault.enc"
    )

    if not vault.exists():

        print(
            "[SKIP] vault.enc absent."
        )

        return True

    original = vault.read_bytes()

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

        success, _ = attack_vault(
            repository
        )

        if not success:

            return False

        detected = run_integrity_check(
            repository
        )

        if not detected:

            print(
                "[FAIL] Vault corruption "
                "was not detected."
            )

            return False

        print(
            "[PASS] Vault corruption detected."
        )

        return True

    finally:

        # ----------------------------------------------------
        # Restauration exacte
        # ----------------------------------------------------

        print(
            "[RESTORE] Restoring vault.enc..."
        )

        if not restore_file(
            vault,
            original,
        ):

            print(
                "[CRITICAL] vault.enc "
                "restoration failed."
            )

        else:

            restored_hash = sha256_file(
                vault
            )

            import hashlib

            original_hash = (
                hashlib.sha256(original)
                .hexdigest()
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

        (
            repository
            / ".security-baseline.json"
        ).unlink(
            missing_ok=True
        )


# ============================================================
# Vérification Git
# ============================================================

def verify_git_clean(
    repository: Path,
) -> bool:

    print(
        "\n=== GIT STATE CHECK ==="
    )

    status = run(
        [
            "git",
            "status",
            "--porcelain",
        ],
        cwd=repository,
        check=False,
    )

    if status.stdout:

        print(
            status.stdout
        )

    # --------------------------------------------------------
    # Vérification des fichiers suivis.
    # --------------------------------------------------------

    tracked_diff = run(
        [
            "git",
            "diff",
            "--exit-code",
        ],
        cwd=repository,
        check=False,
    )

    if tracked_diff.returncode != 0:

        print(
            "[FAIL] Tracked repository "
            "files were modified."
        )

        return False

    print(
        "[PASS] No tracked source "
        "modification remains."
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
        "RED TEAM FILE INTEGRITY TEST"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # Vérifications environnement
    # --------------------------------------------------------

    if not REPOSITORY:

        print(
            "[ERROR] GITHUB_REPOSITORY "
            "is missing."
        )

        return 2

    if not SHA:

        print(
            "[ERROR] GITHUB_SHA "
            "is missing."
        )

        return 2

    if not INTEGRITY_CHECKER.exists():

        print(
            "[ERROR] Integrity checker "
            "not found:"
        )

        print(
            INTEGRITY_CHECKER
        )

        return 2

    # --------------------------------------------------------
    # Scénarios
    # --------------------------------------------------------

    results: list[tuple[str, bool]] = []

    with tempfile.TemporaryDirectory(
        prefix="the_last_signal_attack_"
    ) as temporary_directory:

        repository = (
            Path(temporary_directory)
            / "repository"
        )

        # ====================================================
        # Clone
        # ====================================================

        clone_repository(
            repository
        )

        # ====================================================
        # Création du laboratoire
        # ====================================================

        create_test_environment_files(
            repository
        )

        # ====================================================
        # 1 - Cargo.lock
        # ====================================================

        result = execute_integrity_attack(
            "Cargo.lock tampering",
            repository,
            attack_cargo_lock,
        )

        results.append(
            ("Cargo.lock", result)
        )

        # ====================================================
        # 2 - .env
        # ====================================================

        result = execute_integrity_attack(
            ".env tampering",
            repository,
            attack_env,
        )

        results.append(
            (".env", result)
        )

        # ====================================================
        # 3 - .idea
        # ====================================================

        result = execute_integrity_attack(
            ".idea tampering",
            repository,
            attack_idea,
        )

        results.append(
            (".idea", result)
        )

        # ====================================================
        # 4 - Accès security/
        # ====================================================

        result = attack_security_access(
            repository
        )

        results.append(
            ("security access", result)
        )

        # ====================================================
        # 5 - Modification security/
        # ====================================================

        security_target = (
            repository
            / "security"
        )

        if not security_target.exists():

            security_target = (
                repository
                / "tests"
                / "security"
            )

        if security_target.exists():

            result = execute_integrity_attack(
                "security directory tampering",
                repository,
                attack_security_file,
            )

            results.append(
                ("security tampering", result)
            )

        else:

            print(
                "[SKIP] No security directory."
            )

        # ====================================================
        # 6 - vault.enc
        # ====================================================

        result = execute_vault_attack(
            repository
        )

        results.append(
            ("vault.enc", result)
        )

        # ====================================================
        # 7 - master.key
        # ====================================================

        result = (
            attack_master_key_discovery(
                repository
            )
        )

        results.append(
            ("master.key exposure", result)
        )

        # ====================================================
        # Vérification finale
        # ====================================================

        git_ok = verify_git_clean(
            repository
        )

    # ========================================================
    # Résultat
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
        else:
            print(f"[DEBUG] Scenario failed: {name}")

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

    # --------------------------------------------------------
    # Résultat global
    # --------------------------------------------------------

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
