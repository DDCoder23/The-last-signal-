import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.sax.saxutils as saxutils
from datetime import datetime, timedelta, timezone
from pathlib import Path

OWNER = "The-last-signal-project"
REPO = "The-last-signal-"

API = f"https://api.github.com/repos/{OWNER}/{REPO}"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path("stats/repository-stats.svg")


# --------------------------------------------------
# API GITHUB
# --------------------------------------------------

def api_get(endpoint, params=None):
    """Récupère des données GitHub avec gestion des réponses temporaires."""
    url = API + endpoint

    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "The-Last-Signal-Stats",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(url, headers=headers)

    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else None

        except urllib.error.HTTPError as error:
            if error.code == 202:
                print(f"Statistiques en cours de calcul : {endpoint}")
                if attempt < 5:
                    time.sleep(10)
                    continue
                return None

            if error.code == 204:
                return None

            if error.code == 403 and error.headers.get(
                "X-RateLimit-Remaining"
            ) == "0":
                raise RuntimeError("Limite de requêtes GitHub atteinte.")

            if error.code == 404:
                raise RuntimeError(
                    f"Endpoint introuvable : {endpoint}. "
                    "Vérifie le propriétaire et le nom du dépôt."
                )

            raise RuntimeError(
                f"Erreur API GitHub : HTTP {error.code} sur {endpoint}"
            ) from error

        except urllib.error.URLError as error:
            if attempt < 5:
                time.sleep(3)
                continue
            raise RuntimeError(f"Connexion à GitHub impossible : {error}") from error

    return None


def api_pages(endpoint, params=None, max_pages=10):
    """Récupère plusieurs pages de résultats."""
    results = []

    for page in range(1, max_pages + 1):
        query = dict(params or {})
        query["per_page"] = 100
        query["page"] = page

        data = api_get(endpoint, query)

        if not isinstance(data, list):
            break

        results.extend(data)

        if len(data) < 100:
            break

    return results


# --------------------------------------------------
# STATISTIQUES
# --------------------------------------------------

def get_commit_fallback():
    """Compte les commits récents si les statistiques hebdomadaires manquent."""
    since = (
        datetime.now(timezone.utc) - timedelta(weeks=52)
    ).isoformat()

    commits = api_pages(
        "/commits",
        params={"since": since},
        max_pages=10,
    )

    weekly = [0] * 52
    now = datetime.now(timezone.utc)

    for commit in commits:
        date = (
            commit.get("commit", {})
            .get("committer", {})
            .get("date")
        )

        if not date:
            continue

        try:
            committed_at = datetime.fromisoformat(
                date.replace("Z", "+00:00")
            )
            weeks_ago = (now - committed_at).days // 7

            if 0 <= weeks_ago < 52:
                weekly[51 - weeks_ago] += 1
        except ValueError:
            continue

    return sum(weekly), weekly


def get_statistics():
    repo = api_get("")

    activity = api_get("/stats/commit_activity")
    frequency = api_get("/stats/code_frequency")
    contributors = api_get("/stats/contributors")

    # Commits : statistiques hebdomadaires ou solution de secours.
    if isinstance(activity, list) and activity:
        weekly = [week.get("total", 0) for week in activity[-52:]]
        commits = sum(weekly)
        commits_source = "GitHub weekly statistics"
    else:
        commits, weekly = get_commit_fallback()
        commits_source = "Recent commits fallback"

    # Contributeurs : endpoint statistique, puis liste des contributeurs.
    if isinstance(contributors, list) and contributors:
        contributor_count = len(contributors)
        contributor_source = "GitHub statistics"
    else:
        contributor_list = api_pages(
            "/contributors",
            params={"anon": "true"},
            max_pages=10,
        )
        contributor_count = (
            len(contributor_list) if contributor_list else None
        )
        contributor_source = (
            "Contributors API" if contributor_list else "Unavailable"
        )

    # Modifications du code : N/A si GitHub n'a pas fourni les données.
    additions = None
    deletions = None

    if isinstance(frequency, list) and frequency:
        additions = sum(
            max(0, row[1])
            for row in frequency
            if isinstance(row, list) and len(row) >= 3
        )
        deletions = sum(
            abs(min(0, row[2]))
            for row in frequency
            if isinstance(row, list) and len(row) >= 3
        )

    return {
        "commits": commits,
        "weekly": weekly,
        "contributors": contributor_count,
        "additions": additions,
        "deletions": deletions,
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "issues": repo.get("open_issues_count", 0),
        "language": repo.get("language") or "Not detected",
        "commits_source": commits_source,
        "contributors_source": contributor_source,
    }


# --------------------------------------------------
# DESSIN SVG
# --------------------------------------------------

def esc(value):
    return saxutils.escape(str(value))


def text(x, y, value, size=12, color="#c9d1d9",
         weight="normal", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" '
        f'font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}">{esc(value)}</text>'
    )


def rect(x, y, width, height, fill,
         radius=10, stroke=None):
    border = f' stroke="{stroke}"' if stroke else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" '
        f'height="{height}" rx="{radius}" '
        f'fill="{fill}"{border}/>'
    )


def number(value):
    if value is None:
        return "N/A"
    return f"{value:,}"


def generate_svg(stats):
    width, height = 920, 440

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<title>The Last Signal Repository Statistics</title>',
        '<desc>Statistiques exclusives du dépôt GitHub.</desc>',
        rect(0, 0, width, height, "#0d1117", 18),
        text(30, 40, "The Last Signal", 25, "#f0f6fc", "bold"),
        text(30, 63, "REPOSITORY ANALYTICS", 11, "#8b949e"),
        text(
            890, 40, f"{OWNER}/{REPO}",
            10, "#8b949e", anchor="end"
        ),
    ]

    cards = [
        ("COMMITS · 52 WEEKS", number(stats["commits"]), "#58a6ff"),
        ("CONTRIBUTORS", number(stats["contributors"]), "#3fb950"),
        ("LINES ADDED", number(stats["additions"]), "#3fb950"),
        ("LINES DELETED", number(stats["deletions"]), "#f85149"),
        ("STARS", number(stats["stars"]), "#d29922"),
        ("FORKS", number(stats["forks"]), "#bc8cff"),
    ]

    card_width = 276
    card_height = 72
    start_x = 24
    start_y = 82
    gap_x = 22
    gap_y = 10

    for index, (label, value, color) in enumerate(cards):
        col = index % 3
        row = index // 3

        x = start_x + col * (card_width + gap_x)
        y = start_y + row * (card_height + gap_y)

        parts.append(rect(
            x, y, card_width, card_height,
            "#161b22", 10, "#30363d"
        ))
        parts.append(text(
            x + 15, y + 23, label, 10, "#8b949e", "bold"
        ))
        parts.append(text(
            x + 15, y + 53, value, 22, color, "bold"
        ))

    parts.append(text(
        30, 258, "Weekly commits · last 12 weeks",
        14, "#c9d1d9", "bold"
    ))

    bars = stats["weekly"][-12:]
    max_bar = max(bars, default=0) or 1

    base_y = 365
    bar_width = 45
    gap = 25

    for index, value in enumerate(bars):
        x = 38 + index * (bar_width + gap)
        bar_height = max(2, int(65 * value / max_bar))
        y = base_y - bar_height

        parts.append(rect(
            x, y, bar_width, bar_height, "#388bfd", 5
        ))
        parts.append(text(
            x + bar_width / 2, y - 6,
            value, 10, "#c9d1d9", anchor="middle"
        ))

    parts.append(text(
        30, 400,
        f"Main language: {stats['language']}",
        11, "#8b949e"
    ))
    parts.append(text(
        890, 400,
        f"Open issues: {stats['issues']}",
        11, "#8b949e", anchor="end"
    ))
    parts.append(text(
        30, 423,
        "Updated " + datetime.now(timezone.utc).strftime("%Y-%m-%d UTC"),
        10, "#8b949e"
    ))
    parts.append(text(
        890, 423,
        "Data provided by GitHub API",
        10, "#8b949e", anchor="end"
    ))

    parts.append("</svg>")
    return "\n".join(parts)


# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

def main():
    print(f"Repository: {OWNER}/{REPO}")

    stats = get_statistics()

    print("Commits:", stats["commits"])
    print("Commits source:", stats["commits_source"])
    print("Contributors:", stats["contributors"])
    print("Contributors source:", stats["contributors_source"])
    print("Lines added:", stats["additions"])
    print("Lines deleted:", stats["deletions"])
    print("Stars:", stats["stars"])
    print("Forks:", stats["forks"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(generate_svg(stats), encoding="utf-8")

    print(f"SVG generated successfully: {OUT}")


if __name__ == "__main__":
    main()
