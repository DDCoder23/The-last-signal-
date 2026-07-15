from pathlib import Path

MAX_SCORE = 15

SCORES = {
    "single_h1": 3,
    "heading_order": 3,
    "heading_spacing": 2,
    "empty_titles": 2,
    "title_length": 2,
    "duplicate_titles": 3,
}


def check_titles():

    files = list(Path(".").rglob("*.md"))

    if not files:
        return {
            "score": 0,
            "max_score": MAX_SCORE,
            "results": {},
            "problems": [{
                "severity": "warning",
                "message": "Aucun fichier Markdown trouvé."
            }]
        }

    problems = []
    results = {}

    results["single_h1"] = check_single_h1(files, problems)
    results["heading_order"] = check_heading_order(files, problems)
    results["heading_spacing"] = check_heading_spacing(files, problems)
    results["empty_titles"] = check_empty_titles(files, problems)
    results["title_length"] = check_title_length(files, problems)
    results["duplicate_titles"] = check_duplicate_titles(files, problems)

    return {
        "score": sum(results.values()),
        "max_score": MAX_SCORE,
        "results": results,
        "problems": problems
    }
