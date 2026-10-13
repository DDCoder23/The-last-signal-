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


def esc(value):
    """Échappe les caractères spéciaux pour le XML/SVG."""
    return saxutils.escape(str(value))


def api_get(endpoint):
    """Récupère les données de l'API GitHub."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(API + endpoint, headers=headers)

    for attempt in range(8):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as error:
            if error.code == 202 and attempt < 7:
                time.sleep(5)
                continue

            raise RuntimeError(
                f"Erreur API GitHub sur {endpoint}: HTTP {error.code}"
            ) from error

    raise RuntimeError(f"Statistiques indisponibles : {endpoint}")


def text_element(x, y, content, size=12, color="#c9d1d9",
                 weight="normal", anchor="start"):
    """Construit un élément texte SVG valide."""
    return (
        f'<text x="{x}" y="{y}" '
        f'fill="{color}" '
        f'font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" '
        f'font-weight="{weight}" '
        f'text-anchor="{anchor}">'
        f'{esc(content)}</text>'
    )


def rect(x, y, width, height, fill, radius=10, stroke=None):
    """Construit un rectangle SVG."""
    border = f' stroke="{stroke}"' if stroke else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}"{border}/>'
    )


def format_number(number):
    return f"{number:,}"


def main():
    print(f"Récupération des statistiques de {OWNER}/{REPO}...")

    repo = api_get("")
    activity = api_get("/stats/commit_activity") or []
    frequency = api_get("/stats/code_frequency") or []
    contributors = api_get("/stats/contributors") or []

    # Activité hebdomadaire sur les 52 dernières semaines disponibles.
    weekly_commits = [week.get("total", 0) for week in activity]
    commits_year = sum(weekly_commits)

    # Ajouts et suppressions selon les données hebdomadaires de GitHub.
    additions = sum(max(0, row[1]) for row in frequency if len(row) >= 3)
    deletions = sum(abs(min(0, row[2])) for row in frequency if len(row) >= 3)

    contributor_count = len(contributors)
    all_time_commits = sum(c.get("total", 0) for c in contributors)

    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    open_issues = repo.get("open_issues_count", 0)
    language = repo.get("language") or "Non renseigné"

    # Les douze dernières semaines.
    bars = weekly_commits[-12:]
    max_bar = max(bars, default=0) or 1

    width = 920
    height = 430
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<title>Statistiques du dépôt The Last Signal</title>',
        '<desc>Commits, contributeurs, lignes modifiées et activité du dépôt.</desc>',
        rect(0, 0, width, height, "#0d1117", 18),
        text_element(32, 42, "The Last Signal", 25, "#f0f6fc", "bold"),
        text_element(32, 66, "REPOSITORY STATISTICS", 11, "#8b949e"),
        text_element(
            888, 42, f"{OWNER}/{REPO}", 10, "#8b949e", anchor="end"
        ),
    ]

    # Six indicateurs propres au dépôt.
    cards = [
        ("COMMITS · 52 WEEKS", format_number(commits_year), "#58a6ff"),
        ("CONTRIBUTORS", format_number(contributor_count), "#3fb950"),
        ("LINES ADDED", format_number(additions), "#3fb950"),
        ("LINES DELETED", format_number(deletions), "#f85149"),
        ("STARS", format_number(stars), "#d29922"),
        ("OPEN ISSUES", format_number(open_issues), "#bc8cff"),
    ]

    card_width = 270
    card_height = 78
    start_x = 32
    start_y = 88
    gap_x = 18
    gap_y = 12

    for index, (label, value, color) in enumerate(cards):
        col = index % 3
        row = index // 3
        x = start_x + col * (card_width + gap_x)
        y = start_y + row * (card_height + gap_y)

        parts.append(rect(
            x, y, card_width, card_height,
            "#161b22", 10, "#30363d"
        ))
        parts.append(text_element(
            x + 16, y + 25, label, 10, "#8b949e", "bold"
        ))
        parts.append(text_element(
            x + 16, y + 57, value, 23, color, "bold"
        ))

    # Graphique d'activité.
    chart_top = 280
    chart_bottom = 375
    chart_left = 42

    parts.append(text_element(
        32, 275, "Weekly commits · last 12 weeks",
        14, "#c9d1d9", "bold"
    ))

    bar_width = 48
    gap = 22

    for index, value in enumerate(bars):
        x = chart_left + index * (bar_width + gap)
        bar_height = max(3, int(70 * value / max_bar))
        y = chart_bottom - bar_height

        parts.append(rect(
            x, y, bar_width, bar_height, "#388bfd", 5
        ))
        parts.append(text_element(
            x + bar_width / 2, y - 7,
            value, 10, "#c9d1d9", anchor="middle"
        ))

    # Informations complémentaires.
    parts.append(text_element(
        32, 405,
        f"Recognized commits: {format_number(all_time_commits)}",
        11, "#8b949e"
    ))
    parts.append(text_element(
        32, 422,
        f"Main language: {language}  |  Forks: {forks}",
        11, "#8b949e"
    ))
    parts.append(text_element(
        888, 405,
        "Updated " + datetime.now(timezone.utc).strftime("%Y-%m-%d UTC"),
        10, "#8b949e", anchor="end"
    ))

    parts.append("</svg>")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")

    print(f"Carte générée : {OUT}")
    print(f"Commits sur 52 semaines : {commits_year}")
    print(f"Contributeurs : {contributor_count}")
    print(f"Lignes ajoutées : {additions}")
    print(f"Lignes supprimées : {deletions}")


if __name__ == "__main__":
    main()
