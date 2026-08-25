```python id="7e4x9k"
from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

BASELINE_FILE = ".security-baseline.json"

# Répertoires complètement exclus du scan.
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

# Fichiers exclus du scan.
IGNORED_FILES = {
    BASELINE_FILE,
}

# Extensions considérées comme sensibles au niveau intégrité.
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
    ".pem",
    ".key",
    ".p12",
    ".pfx",
}

# Fichiers sensibles surveillés explicitement.
WATCHED_SPECIAL_FILES = {
    ".env",
    "Cargo.lock",
    "Cargo.toml",
    "vault.enc",
    "master.key",
    "id_rsa",
    "id_ed25519",
    "id_ecdsa",
    "id_dsa",
}

# Répertoires dont tous les fichiers sont surveillés.
WATCHED_DIRECTORIES = {
    ".github",
    ".idea",
    "security",
}

# Taille maximale d'un fichier que ce scanner acceptera.
#
# Cela évite qu'un test d'intégrité tente de charger un énorme
# fichier accidentellement ajouté au dépôt.
MAX_FILE_SIZE = 256 * 1024 * 1024  # 256 MiB


# ============================================================
# Exceptions
# ============================================================

class IntegrityError(RuntimeError):
    """Erreur interne du vérificateur d'intégrité."""


# ============================================================
# SHA-256
# ============================================================

def sha256_file(path: Path) -> str:
    """
    Calcule le SHA-256 d'un fichier.

    Le fichier est lu par blocs pour éviter de charger
    l'intégralité du contenu en mémoire.
    """

    try:
        file_size = path.stat().st_size

    except OSError as error:
        raise IntegrityError(
            f"Impossible d'obtenir la taille de {path}: {error}"
        ) from error

    if file_size > MAX_FILE_SIZE:
        raise IntegrityError(
            f"Fichier trop volumineux pour le scan: {path}"
        )

    digest = hashlib.sha256()

    try:
        with path.open("rb") as file:

            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

    except OSError as error:
        raise IntegrityError(
            f"Impossible de lire {path}: {error}"
        ) from error

    return digest.hexdigest()


# ============================================================
# Path helpers
# ============================================================

def relative_path(
    path: Path,
    root: Path,
) -> Path:

    try:
        return path.relative_to(root)

    except ValueError as error:
        raise IntegrityError(
            f"Path outside repository: {path}"
        ) from error


def is_path_ignored(
    path: Path,
    root: Path,
) -> bool:

    relative = relative_path(
        path,
        root,
    )

    if path.name in IGNORED_FILES:
        return True

    return any(
        part in IGNORED_DIRECTORIES
        for part in relative.parts
    )


# ============================================================
# Symlinks
# ============================================================

def is_symlink(path: Path) -> bool:
    """
    Retourne True si path est un lien symbolique.

    Les symlinks sont volontairement traités comme des éléments
    suspects plutôt que suivis aveuglément.
    """

    try:
        return path.is_symlink()

    except OSError as error:
        raise IntegrityError(
            f"Impossible d'inspecter {path}: {error}"
        ) from error


# ============================================================
# Détermination des fichiers surveillés
# ============================================================

def is_watched(
    path: Path,
    root: Path,
) -> bool:

    relative = relative_path(
        path,
        root,
    )

    # --------------------------------------------------------
    # Fichiers sensibles explicites
    # --------------------------------------------------------

    if path.name in WATCHED_SPECIAL_FILES:
        return True

    # --------------------------------------------------------
    # Répertoires sensibles
    # --------------------------------------------------------

    for part in relative.parts:

        if part in WATCHED_DIRECTORIES:
            return True

    # --------------------------------------------------------
    # Extensions
    # --------------------------------------------------------

    if path.suffix.lower() in WATCHED_EXTENSIONS:
        return True

    return False


# ============================================================
# Scan du dépôt
# ============================================================

def scan_repository(
    root: Path,
) -> dict[str, str]:

    """
    Retourne :

        chemin relatif POSIX -> SHA-256

    Exemple :

        {
            "src/main.py": "...",
            "Cargo.lock": "...",
        }

    Les erreurs de lecture sont considérées comme des erreurs
    critiques plutôt que silencieusement ignorées.
    """

    root = root.resolve()

    if not root.is_dir():
        raise IntegrityError(
            f"Repository directory not found: {root}"
        )

    result: dict[str, str] = {}

    # --------------------------------------------------------
    # os.walk permet de contrôler les répertoires ignorés
    # avant de les parcourir.
    # --------------------------------------------------------

    for current_root, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):

        current = Path(current_root)

        # ----------------------------------------------------
        # Ne jamais entrer dans les répertoires ignorés.
        # ----------------------------------------------------

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in files:

            path = current / filename

            if is_path_ignored(
                path,
                root,
            ):
                continue

            # ------------------------------------------------
            # Symlink :
            #
            # Ne pas suivre un lien vers l'extérieur.
            # ------------------------------------------------

            if is_symlink(path):

                if is_watched(
                    path,
                    root,
                ):

                    relative = (
                        relative_path(
                            path,
                            root,
                        )
                        .as_posix()
                    )

                    raise IntegrityError(
                        "Watched path is a symbolic link: "
                        f"{relative}"
                    )

                continue

            # ------------------------------------------------
            # Seulement les fichiers surveillés.
            # ------------------------------------------------

            if not is_watched(
                path,
                root,
            ):
                continue

            relative = (
                relative_path(
                    path,
                    root,
                )
                .as_posix()
            )

            result[relative] = sha256_file(
                path
            )

    return dict(
        sorted(
            result.items()
        )
    )


# ============================================================
# Validation SHA
# ============================================================

def validate_sha(
    value: object,
) -> bool:

    if not isinstance(
        value,
        str,
    ):
        return False

    if len(value) != 64:
        return False

    return all(
        character in "0123456789abcdef"
        for character in value.lower()
    )


# ============================================================
# Validation des chemins de baseline
# ============================================================

def validate_baseline_path(
    value: object,
) -> bool:

    if not isinstance(
        value,
        str,
    ):
        return False

    if not value:
        return False

    path = Path(value)

    # Un chemin de baseline doit être relatif.
    if path.is_absolute():
        return False

    # Normalisation POSIX utilisée par le scanner.
    normalized = value.replace(
        "\\",
        "/",
    )

    parts = Path(normalized).parts

    if ".." in parts:
        return False

    if normalized.startswith("/"):
        return False

    return True


# ============================================================
# Validation baseline
# ============================================================

def validate_baseline(
    baseline: object,
) -> dict[str, str]:

    if not isinstance(
        baseline,
        dict,
    ):
        raise IntegrityError(
            "Baseline must contain a JSON object."
        )

    validated: dict[str, str] = {}

    for path, digest in baseline.items():

        if not validate_baseline_path(
            path
        ):
            raise IntegrityError(
                f"Invalid baseline path: {path!r}"
            )

        if not validate_sha(
            digest
        ):
            raise IntegrityError(
                f"Invalid SHA-256 for: {path!r}"
            )

        validated[path] = digest.lower()

    return dict(
        sorted(
            validated.items()
        )
    )


# ============================================================
# Baseline
# ============================================================

def save_baseline(
    root: Path,
    baseline: dict[str, str],
) -> None:

    path = root / BASELINE_FILE

    data = {
        "version": 2,
        "algorithm": "sha256",
        "files": baseline,
    }

    try:

        path.write_text(
            json.dumps(
                data,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    except OSError as error:

        raise IntegrityError(
            f"Unable to write baseline: {error}"
        ) from error


def load_baseline(
    root: Path,
) -> dict[str, str]:

    path = root / BASELINE_FILE

    if not path.is_file():
        raise IntegrityError(
            f"Baseline missing: {path}"
        )

    try:

        raw = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except (OSError, UnicodeError) as error:

        raise IntegrityError(
            f"Unable to read baseline: {error}"
        ) from error

    except json.JSONDecodeError as error:

        raise IntegrityError(
            f"Invalid baseline JSON: {error}"
        ) from error

    # --------------------------------------------------------
    # Format v2
    # --------------------------------------------------------

    if not isinstance(
        raw,
        dict,
    ):
        raise IntegrityError(
            "Invalid baseline root."
        )

    if raw.get("version") != 2:
        raise IntegrityError(
            "Unsupported baseline version."
        )

    if raw.get("algorithm") != "sha256":
        raise IntegrityError(
            "Unsupported baseline hashing algorithm."
        )

    files = raw.get("files")

    return validate_baseline(
        files
    )


# ============================================================
# Comparaison
# ============================================================

def compare(
    before: dict[str, str],
    after: dict[str, str],
) -> dict[str, list[str]]:

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
        for path in (
            before_files
            & after_files
        )
        if before[path] != after[path]
    )

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
    }


# ============================================================
# Création baseline
# ============================================================

def create(
    root: Path,
) -> int:

    print(
        "=== SECURITY BASELINE ==="
    )

    try:

        baseline = scan_repository(
            root
        )

        save_baseline(
            root,
            baseline,
        )

    except IntegrityError as error:

        print(
            f"[ERROR] {error}",
            file=sys.stderr,
        )

        return 2

    print(
        f"Files monitored: {len(baseline)}"
    )

    print(
        f"Baseline: {BASELINE_FILE}"
    )

    return 0


# ============================================================
# Affichage différences
# ============================================================

def print_differences(
    differences: dict[str, list[str]],
) -> int:

    added = differences["added"]
    removed = differences["removed"]
    modified = differences["modified"]

    total = (
        len(added)
        + len(removed)
        + len(modified)
    )

    # --------------------------------------------------------
    # Ajouts
    # --------------------------------------------------------

    if added:

        print("\n[ADDED]")

        for path in added:
            print(
                f"  + {path}"
            )

    # --------------------------------------------------------
    # Suppressions
    # --------------------------------------------------------

    if removed:

        print("\n[REMOVED]")

        for path in removed:
            print(
                f"  - {path}"
            )

    # --------------------------------------------------------
    # Modifications
    # --------------------------------------------------------

    if modified:

        print("\n[MODIFIED]")

        for path in modified:
            print(
                f"  * {path}"
            )

    return total


# ============================================================
# Vérification intégrité
# ============================================================

def check(
    root: Path,
) -> int:

    print(
        "=== INTEGRITY CHECK ==="
    )

    try:

        before = load_baseline(
            root
        )

        after = scan_repository(
            root
        )

        differences = compare(
            before,
            after,
        )

    except IntegrityError as error:

        print(
            f"\n[ERROR] {error}",
            file=sys.stderr,
        )

        return 2

    total = print_differences(
        differences
    )

    if total == 0:

        print(
            "\n[PASS] "
            "No integrity violation detected."
        )

        return 0

    print(
        f"\n[FAIL] "
        f"{total} integrity violation(s) detected."
    )

    return 1


# ============================================================
# CLI
# ============================================================

def print_usage() -> None:

    print(
        "Usage:\n"
        "  python integrity_check.py create\n"
        "  python integrity_check.py check"
    )


def main() -> int:

    if len(sys.argv) != 2:

        print_usage()

        return 2

    root = Path.cwd().resolve()

    command = sys.argv[1]

    if command == "create":

        return create(
            root
        )

    if command == "check":

        return check(
            root
        )

    print(
        f"Unknown command: {command}"
    )

    print_usage()

    return 2


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    raise SystemExit(
        main()
    )
```
