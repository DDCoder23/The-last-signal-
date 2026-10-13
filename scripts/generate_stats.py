import json
import os
import time
import urllib.error
import urllib.request
import xml.sax.saxutils as saxutils
from datetime import datetime, timezone
from pathlib import Path

OWNER = "The-last-signal-project"
REPO = "The-last-signal-"
API = f"https://api.github.com/repos/{OWNER}/{REPO}"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path("stats/repository-stats.svg")


def api_get(endpoint):
    request = urllib.request.Request(
        API + endpoint,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )

    for attempt in range(8):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            # GitHub calcule certaines statistiques en arrière-plan.
            if error.code == 202 and attempt < 7:
                time.sleep(5)
                continue
            raise RuntimeError(
                f"GitHub API {endpoint}: HTTP {error.code}"
            ) from error

    raise RuntimeError(f"Statistiques indisponibles : {endpoint}")


def esc(value):
    return saxutils.escape(str(value))


def main():
    repo = api_get("")
    activity = api_get("/stats/commit_activity") or []
    frequency = api_get("/stats/code_frequency") or []
    contributors = api_get("/stats/contributors") or []

    # Activité des 52 dernières semaines.
    weekly_commits = [week.get("total", 0) for week in activity]
    commits_year = sum(weekly_commits)

    # Ajouts et suppressions fournis par GitHub,
    # agrégés par semaine sur l'historique disponible.
    additions = sum(max(0, row[1]) for row in frequency)
    deletions = sum(abs(min(0, row[2])) for row in frequency)

    # Contributeurs et commits reconnus par GitHub.
    contributor_count = len(contributors)
    all_time_commits = sum(c.get("total", 0) for c in contributors)

    # Conserve uniquement les 12 dernières semaines pour le graphique.
    bars = weekly_commits[-12:]
    max_bar = max(bars, default=0) or 1

    width, height = 920, 380
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" rx="18" fill="#0d1117"/>',
        '<text x="32" y="42" fill="#c9d1d9" '
        'font-family="Arial,sans-serif" font-size="23" '
        'font-weight="bold">The Last Signal</text>',
        '<text x="32" y="66" fill="#8b949e" '
        'font-family="Arial,sans-serif" font-size="12">'
        'REPOSITORY STATISTICS</text>',
    ]

    cards = [
        ("COMMITS · 52 WEEKS", f"{commits_year:,}"),
        ("CONTRIBUTORS", f"{contributor_count:,}"),
        ("LINES ADDED · HISTORY", f"{additions:,}"),
        ("LINES DELETED · HISTORY", f"{deletions:,}"),
    ]

    for index, (label, value) in enumerate(cards):
        x = 32 + index * 220
        parts += [
            f'<rect x="{x}" y="88" width="204" height="92" '
            'rx="10" fill="#161b22" stroke="#30363d"/>',
            f'<text x="{x + 15}" y="115" fill="#8b949e" '
            'font-family="Arial,sans-serif" font-size="10">'
            f'{esc(label)}</text>',
            f'<text x="{x + 15}" y="153" fill="#58a6ff" '
            'font-family="Arial,sans-serif" font-size="24" '
            'font-weight="bold">{esc(value)}</text>',
        ]

    parts += [
        '<text x="32" y="220" fill="#c9d1d9" '
        'font-family="Arial,sans-serif" font-size="15">'
        'Weekly commits · last 12 weeks</text>',
    ]

    bar_width = 48
    gap = 18
    base_y = 330

    for index, value in enumerate(bars):
        x = 42 + index * (bar_width + gap)
        bar_height = max(3, int(80 * value / max_bar))
        y = base_y - bar_height

        parts += [
            f'<rect x="{x}" y="{y}" width="{bar_width}" '
            f'height="{bar_height}" rx="5" fill="#58a6ff"/>',
            f'<text x="{x + bar_width / 2}" y="{base_y + 18}" '
            'text-anchor="middle" fill="#8b949e" '
            'font-family="Arial,sans-serif" font-size="10">'
            f'{value}</text>',
        ]

    parts += [
        '<text x="32" y="365" fill="#8b949e" '
        'font-family="Arial,sans-serif" font-size="10">'
        f'All-time recognized commits: {all_time_commits:,}'
        '</text>',
        '<text x="888" y="365" text-anchor="end" '
        'fill="#8b949e" font-family="Arial,sans-serif" '
        'font-size="10">'
        f'Updated {datetime.now(timezone.utc).strftime("%Y-%m-%d")} UTC'
        '</text>',
        '</svg>',
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Generated {OUT}")


if __name__ == "__main__":
    main()
