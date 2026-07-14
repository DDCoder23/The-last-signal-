from pathlib import Path


MAX_SCORE = 20


def check_markdown():
    """
    Analyse la qualité globale des fichiers Markdown.

    Returns:
        dict: {
            "score": int,
            "max_score": int,
            "problems": list[str]
        }
    """

    score = 0
    problems = []

    files = list(Path(".").rglob("*.md"))

    if not files:
        return {
            "score": 0,
            "max_score": MAX_SCORE,
            "problems": ["Aucun fichier Markdown trouvé."]
        }

    score += check_empty_files(files, problems)
    score += check_encoding(files, problems)
    score += check_line_length(files, problems)
    score += check_trailing_spaces(files, problems)
    score += check_code_blocks(files, problems)
    score += check_lists(files, problems)
    score += check_tables(files, problems)
    score += check_html(files, problems)

    return {
        "score": score,
        "max_score": MAX_SCORE,
        "problems": problems
    }
