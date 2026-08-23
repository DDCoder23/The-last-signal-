from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

BASELINE_FILE = ".security-baseline.json"

# Répertoires que le scanner ne doit jamais parcourir.
# .git est volontairement exclu : nous ne voulons pas modifier
# les métadonnées Git du clone.
IGNORED_DIRECTORIES = {
    ".git",
    "target",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
}

IGNORED_FILES = {
    BASELINE_FILE,
}

WATCHED_EXTENSIONS = {
    ".py",
    ".rs",
    ".toml",
    ".lock",
    ".sql",
    ".yml",
    ".yaml",
    ".json",
    ".env",
}

WATCHED_SPECIAL_FILES = {
    ".env",
    "Cargo.lock",
    "Cargo.toml",
    "vault.enc",
    "master.key",
}

WATCHED_DIRECTORIES = {
    ".github",
    ".idea",
    "security",
}


# ============================================================
# Hash SHA-256
# ============================================================

def sha256_file(path: Path) -> str:
    """Calcule le SHA-256 d'un fichier."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# Détermination des fichiers surveillés
# ============================================================

def is_watched(path: Path, root: Path) -> bool:
    """
    Détermine si un fichier doit être surveillé.
    """

    relative = path.relative_to(root)

    # Fichiers sensibles explicitement surveillés.
    if path.name in WATCHED_SPECIAL_FILES:
        return True

    # Répertoires sensibles explicitement surveillés.
    for part in relative.parts:
        if part in WATCHED_DIRECTORIES:
            return True

    # Extensions de code/configuration.
    if path.suffix.lower() in WATCHED_EXTENSIONS:
        return True

    return False


def should_ignore(path: Path, root: Path) -> bool:
    """
    Détermine si un fichier/répertoire doit être ignoré.
    """

    relative = path.relative_to(root)

    if path.name in IGNORED_FILES:
        return True

    for part in relative.parts:
        if part in IGNORED_DIRECTORIES:
            return True

    return False


# ============================================================
# Scan du dépôt
# ============================================================

def scan_repository(root: Path) -> dict[str, str]:
    """
    Parcourt le dépôt et retourne :

        chemin relatif -> SHA-256
    """

    result: dict[str, str] = {}

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if should_ignore(path, root):
            continue

        if not is_watched(path, root):
            continue

        relative = path.relative_to(root).as_posix()

        try:
            result[relative] = sha256_file(path)

        except OSError as error:
            print(
                f"[WARN] Impossible de lire {relative}: {error}",
                file=sys.stderr,
            )

    return dict(sorted(result.items()))


# ============================================================
# Baseline
# ============================================================

def save_baseline(
    root: Path,
    baseline: dict[str, str],
) -> None:
    """Sauvegarde la baseline."""

    path = root / BASELINE_FILE

    path.write_text(
        json.dumps(
            baseline,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


def load_baseline(root: Path) -> dict[str, str]:
    """Charge la baseline."""

    path = root / BASELINE_FILE

    if not path.exists():
        raise FileNotFoundError(
            f"Baseline absente : {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


# ============================================================
# Comparaison
# ============================================================

def compare(
    before: dict[str, str],
    after: dict[str, str],
) -> dict[str, list[str]]:
    """
    Compare deux états du dépôt.
    """

    before_files = set(before)
    after_files = set(after)

    added = sorted(
        after_files - before_files
    )

    removed = sorted(
        before_files - after_files
    )

    modified = sorted(
        path
        for path in before_files & after_files
        if before[path] != after[path]
    )

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
    }


# ============================================================
# Création de baseline
# ============================================================

def create(root: Path) -> int:

    print("=== SECURITY BASELINE ===")

    baseline = scan_repository(root)

    save_baseline(
        root,
        baseline,
    )

    print(
        f"Files monitored: {len(baseline)}"
    )

    print(
        f"Baseline: {BASELINE_FILE}"
    )

    return 0


# ============================================================
# Vérification d'intégrité
# ============================================================

def check(root: Path) -> int:

    print("=== INTEGRITY CHECK ===")

    before = load_baseline(root)

    after = scan_repository(root)

    differences = compare(
        before,
        after,
    )

    added = differences["added"]
    removed = differences["removed"]
    modified = differences["modified"]

    # --------------------------------------------------------
    # Fichiers ajoutés
    # --------------------------------------------------------

    if added:
        print("\n[ADDED]")

        for path in added:
            print(f"  + {path}")

    # --------------------------------------------------------
    # Fichiers supprimés
    # --------------------------------------------------------

    if removed:
        print("\n[REMOVED]")

        for path in removed:
            print(f"  - {path}")

    # --------------------------------------------------------
    # Fichiers modifiés
    # --------------------------------------------------------

    if modified:
        print("\n[MODIFIED]")

        for path in modified:
            print(f"  * {path}")

    total = (
        len(added)
        + len(removed)
        + len(modified)
    )

    # --------------------------------------------------------
    # Aucun changement
    # --------------------------------------------------------

    if total == 0:

        print(
            "\n[PASS] No integrity violation detected."
        )

        return 0

    # --------------------------------------------------------
    # Modification détectée
    # --------------------------------------------------------

    print(
        f"\n[FAIL] "
        f"{total} integrity violation(s) detected."
    )

    return 1


# ============================================================
# Main
# ============================================================

def main() -> int:

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "  python integrity_check.py create\n"
            "  python integrity_check.py check"
        )

        return 2

    root = Path.cwd().resolve()

    command = sys.argv[1]

    if command == "create":
        return create(root)

    if command == "check":
        return check(root)

    print(
        f"Unknown command: {command}"
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
