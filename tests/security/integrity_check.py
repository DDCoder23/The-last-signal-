from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

BASELINE_FILE = ".security-baseline.json"

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
}

WATCHED_DIRECTORIES = {
    ".github",
    ".idea",
}


# ============================================================
# Hash
# ============================================================

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# Détection des fichiers surveillés
# ============================================================

def is_watched(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)

    # Fichiers explicitement surveillés.
    if path.name in WATCHED_SPECIAL_FILES:
        return True

    # Répertoires explicitement surveillés.
    for part in relative.parts:
        if part in WATCHED_DIRECTORIES:
            return True

    # Extensions surveillées.
    if path.suffix.lower() in WATCHED_EXTENSIONS:
        return True

    return False


def should_ignore(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)

    if path.name in IGNORED_FILES:
        return True

    for part in relative.parts:
        if part in IGNORED_DIRECTORIES:
            return True

    return False


# ============================================================
# Scan
# ============================================================

def scan_repository(root: Path) -> dict[str, str]:
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

def save_baseline(root: Path, baseline: dict[str, str]) -> None:
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
    path = root / BASELINE_FILE

    if not path.exists():
        raise FileNotFoundError(
            f"Baseline absente: {path}"
        )

    return json.loads(
        path.read_text(encoding="utf-8")
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

    added = sorted(after_files - before_files)
    removed = sorted(before_files - after_files)

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
# Commandes
# ============================================================

def create(root: Path) -> int:
    baseline = scan_repository(root)
    save_baseline(root, baseline)

    print("=== SECURITY BASELINE ===")
    print(f"Files monitored: {len(baseline)}")
    print(f"Baseline: {BASELINE_FILE}")

    return 0


def check(root: Path) -> int:
    before = load_baseline(root)
    after = scan_repository(root)

    differences = compare(before, after)

    added = differences["added"]
    removed = differences["removed"]
    modified = differences["modified"]

    print("=== INTEGRITY CHECK ===")

    if added:
        print("\n[ADDED]")
        for path in added:
            print(f"  + {path}")

    if removed:
        print("\n[REMOVED]")
        for path in removed:
            print(f"  - {path}")

    if modified:
        print("\n[MODIFIED]")
        for path in modified:
            print(f"  * {path}")

    total = len(added) + len(removed) + len(modified)

    if total == 0:
        print("\n[PASS] No integrity violation detected.")
        return 0

    print(
        f"\n[FAIL] {total} integrity violation(s) detected."
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

    print(f"Unknown command: {command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
