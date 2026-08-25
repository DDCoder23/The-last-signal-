from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

BASELINE_VERSION = 3
HASH_ALGORITHM = "sha256"

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
    ".security-baseline.json",
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
    ".pem",
    ".key",
    ".p12",
    ".pfx",
}

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

WATCHED_DIRECTORIES = {
    ".github",
    ".idea",
    "security",
}

MAX_FILE_SIZE = 256 * 1024 * 1024


# ============================================================
# Exception
# ============================================================

class IntegrityError(RuntimeError):
    pass


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


def is_ignored(
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
# SHA-256
# ============================================================

def sha256_file(
    path: Path,
) -> str:

    try:
        size = path.stat().st_size

    except OSError as error:

        raise IntegrityError(
            f"Cannot stat file {path}: {error}"
        ) from error

    if size > MAX_FILE_SIZE:

        raise IntegrityError(
            f"File too large to scan: {path}"
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
            f"Cannot read file {path}: {error}"
        ) from error

    return digest.hexdigest()


# ============================================================
# Watched files
# ============================================================

def is_watched(
    path: Path,
    root: Path,
) -> bool:

    relative = relative_path(
        path,
        root,
    )

    if path.name in WATCHED_SPECIAL_FILES:
        return True

    for part in relative.parts:

        if part in WATCHED_DIRECTORIES:
            return True

    if path.suffix.lower() in WATCHED_EXTENSIONS:
        return True

    return False


# ============================================================
# Repository scan
# ============================================================

def scan_repository(
    root: Path,
) -> dict[str, str]:

    root = root.resolve()

    if not root.is_dir():

        raise IntegrityError(
            f"Repository not found: {root}"
        )

    result: dict[str, str] = {}

    for current_root, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):

        current = Path(current_root)

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in files:

            path = current / filename

            if is_ignored(
                path,
                root,
            ):
                continue

            # ------------------------------------------------
            # Never follow watched symlinks.
            # ------------------------------------------------

            if path.is_symlink():

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
                        "Watched file is a symbolic link: "
                        f"{relative}"
                    )

                continue

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
# Baseline validation
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


def validate_path(
    value: object,
) -> bool:

    if not isinstance(
        value,
        str,
    ):
        return False

    if not value:
        return False

    normalized = value.replace(
        "\\",
        "/",
    )

    path = Path(normalized)

    if path.is_absolute():
        return False

    if normalized.startswith("/"):
        return False

    if ".." in path.parts:
        return False

    return True


def validate_baseline(
    value: object,
) -> dict[str, str]:

    if not isinstance(
        value,
        dict,
    ):

        raise IntegrityError(
            "Baseline files must be a JSON object."
        )

    result: dict[str, str] = {}

    for path, digest in value.items():

        if not validate_path(path):

            raise IntegrityError(
                f"Invalid baseline path: {path!r}"
            )

        if not validate_sha(digest):

            raise IntegrityError(
                f"Invalid SHA-256: {path!r}"
            )

        result[path] = digest.lower()

    return dict(
        sorted(
            result.items()
        )
    )


# ============================================================
# Baseline create
# ============================================================

def save_baseline(
    path: Path,
    files: dict[str, str],
) -> None:

    path = path.resolve()

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {
        "version": BASELINE_VERSION,
        "algorithm": HASH_ALGORITHM,
        "files": files,
    }

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    try:

        temporary.write_text(
            json.dumps(
                data,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        temporary.replace(
            path
        )

    except OSError as error:

        temporary.unlink(
            missing_ok=True
        )

        raise IntegrityError(
            f"Cannot write baseline: {error}"
        ) from error


def load_baseline(
    path: Path,
) -> dict[str, str]:

    path = path.resolve()

    if not path.is_file():

        raise IntegrityError(
            f"Baseline not found: {path}"
        )

    try:

        raw = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:

        raise IntegrityError(
            f"Invalid baseline JSON: {error}"
        ) from error

    except OSError as error:

        raise IntegrityError(
            f"Cannot read baseline: {error}"
        ) from error

    if not isinstance(
        raw,
        dict,
    ):

        raise IntegrityError(
            "Invalid baseline structure."
        )

    if raw.get("version") != BASELINE_VERSION:

        raise IntegrityError(
            "Unsupported baseline version."
        )

    if raw.get("algorithm") != HASH_ALGORITHM:

        raise IntegrityError(
            "Unsupported hashing algorithm."
        )

    return validate_baseline(
        raw.get("files")
    )


# ============================================================
# Comparison
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
# Create
# ============================================================

def create(
    repository: Path,
    baseline_path: Path,
) -> int:

    print("=== SECURITY BASELINE ===")

    try:

        files = scan_repository(
            repository
        )

        save_baseline(
            baseline_path,
            files,
        )

    except IntegrityError as error:

        print(
            f"[ERROR] {error}",
            file=sys.stderr,
        )

        return 2

    print(
        f"Files monitored: {len(files)}"
    )

    print(
        f"Baseline: {baseline_path}"
    )

    return 0


# ============================================================
# Check
# ============================================================

def check(
    repository: Path,
    baseline_path: Path,
) -> int:

    print("=== INTEGRITY CHECK ===")

    try:

        before = load_baseline(
            baseline_path
        )

        after = scan_repository(
            repository
        )

        differences = compare(
            before,
            after,
        )

    except IntegrityError as error:

        print(
            f"[ERROR] {error}",
            file=sys.stderr,
        )

        return 2

    added = differences["added"]
    removed = differences["removed"]
    modified = differences["modified"]

    if added:

        print("\n[ADDED]")

        for path in added:
            print(
                f"  + {path}"
            )

    if removed:

        print("\n[REMOVED]")

        for path in removed:
            print(
                f"  - {path}"
            )

    if modified:

        print("\n[MODIFIED]")

        for path in modified:
            print(
                f"  * {path}"
            )

    total = (
        len(added)
        + len(removed)
        + len(modified)
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

def usage() -> None:

    print(
        "Usage:\n"
        "\n"
        "  python integrity_check.py create "
        "<repository> <baseline>\n"
        "\n"
        "  python integrity_check.py check "
        "<repository> <baseline>"
    )


def main() -> int:

    if len(sys.argv) != 4:

        usage()

        return 2

    command = sys.argv[1]

    repository = Path(
        sys.argv[2]
    ).resolve()

    baseline = Path(
        sys.argv[3]
    ).resolve()

    if command == "create":

        return create(
            repository,
            baseline,
        )

    if command == "check":

        return check(
            repository,
            baseline,
        )

    print(
        f"Unknown command: {command}"
    )

    usage()

    return 2


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
