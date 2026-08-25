from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd().resolve()


SECRET_PATTERNS = [
    re.compile(
        r"-----BEGIN .*PRIVATE KEY-----"
    ),
    re.compile(
        r"\bAKIA[0-9A-Z]{16}\b"
    ),
    re.compile(
        r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"
    ),
    re.compile(
        r"(?i)\bpassword\s*[:=]\s*['\"][^'\"]{6,}"
    ),
    re.compile(
        r"(?i)\bapi[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}"
    ),
]


def run_git(
    arguments: list[str],
) -> subprocess.CompletedProcess[str]:

    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> int:
    print("=== GIT SECURITY SCAN ===")

    failures = 0

    if not (ROOT / ".git").exists():
        print(
            "[SKIP] Not a Git repository."
        )
        return 0

    # --------------------------------------------------------
    # Working tree
    # --------------------------------------------------------

    status = run_git(
        ["status", "--porcelain"]
    )

    if status.returncode != 0:
        print(
            "[WARN] Unable to inspect Git status."
        )
    elif status.stdout.strip():
        print(
            "[INFO] Working tree contains changes."
        )

    # --------------------------------------------------------
    # Sensitive tracked files
    # --------------------------------------------------------

    tracked = run_git(
        ["ls-files"]
    )

    sensitive_names = {
        ".env",
        ".env.local",
        ".env.production",
        "master.key",
        "id_rsa",
        "id_ed25519",
        "credentials.json",
        "service-account.json",
    }

    if tracked.returncode == 0:

        for line in tracked.stdout.splitlines():

            path = Path(line)

            if path.name in sensitive_names:
                print(
                    f"[FAIL] Sensitive file tracked by Git: "
                    f"{line}"
                )
                failures += 1

    # --------------------------------------------------------
    # Git configuration
    # --------------------------------------------------------

    config = run_git(
        ["config", "--get", "core.filemode"]
    )

    if config.returncode == 0:
        value = config.stdout.strip()

        print(
            f"[INFO] core.filemode={value}"
        )

    # --------------------------------------------------------
    # Current commit
    # --------------------------------------------------------

    commit = run_git(
        [
            "rev-parse",
            "HEAD",
        ]
    )

    if commit.returncode == 0:
        print(
            f"[INFO] HEAD={commit.stdout.strip()}"
        )

    # --------------------------------------------------------
    # Scan history for obvious secrets.
    #
    # Important:
    # We do not print matching lines.
    # --------------------------------------------------------

    print(
        "[INFO] Scanning Git history for obvious secrets..."
    )

    history = run_git(
        [
            "log",
            "--all",
            "--format=",
            "-p",
            "--no-ext-diff",
        ]
    )

    if history.returncode != 0:
        print(
            "[WARN] Git history scan unavailable."
        )
    else:

        for line in history.stdout.splitlines():

            if any(
                pattern.search(line)
                for pattern in SECRET_PATTERNS
            ):
                print(
                    "[FAIL] Potential secret detected "
                    "in Git history."
                )

                failures += 1

                # Une seule occurrence suffit à signaler
                # le problème.
                break

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    if failures == 0:
        print(
            "[PASS] Git security checks passed."
        )
        return 0

    print(
        f"[FAIL] {failures} Git security issue(s) detected."
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
