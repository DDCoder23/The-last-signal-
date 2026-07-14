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

    results = {}

    results["empty_files"] = check_empty_files(files, problems)
    results["encoding"] = check_encoding(files, problems)
    results["line_length"] = check_line_length(files, problems)
    results["trailing_spaces"] = check_trailing_spaces(files, problems)
    results["code_blocks"] = check_code_blocks(files, problems)
    results["lists"] = check_lists(files, problems)
    results["tables"] = check_tables(files, problems)
    results["html"] = check_html(files, problems)

    score = sum(results.values())

    return {
    "score": score,
    "max_score": MAX_SCORE,
    "results": results,
    "problems": problems
}

    





def check_empty_files(files: list[Path], problems: list[dict]) -> int:
    """
    Vérifie la qualité du contenu des fichiers Markdown.

    Retourne un score sur 3.
    """

    empty_files = []
    almost_empty = []

    for file in files:

        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            ).strip()

        except Exception:
            problems.append({"file" : str(file),
                             "message": "fichier illisible"})
            empty_files.append(file)
            continue

        # Fichier complètement vide
        if not content:
            empty_files.append(file)
            continue

        # Nombre de caractères utiles
        useful_chars = len(content)

        # Nombre de lignes utiles
        useful_lines = [
            line
            for line in content.splitlines()
            if line.strip()
        ]

        # Fichier très pauvre
        if useful_chars < 50 or len(useful_lines) < 3:
            almost_empty.append(file)

    for file in empty_files:
        problems.append({"file" : str(file),
                         "message": "fichier vide"})
            

    for file in almost_empty:
        problems.append({"file" : str(file),
                         "message": "fichier quasiment vide"})

    penalty = (
        len(empty_files) * 1
        +
        len(almost_empty) * 0.5
    )

    ratio = max(
        0,
        1 - penalty / len(files)
    )

    return round(ratio * 3)
