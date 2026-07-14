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
def check_encoding(files, problems):
    """
    Vérifie que tous les fichiers sont encodés en UTF-8.
    """

    invalid = 0

    for file in files:

        try:
            file.read_text(encoding="utf-8")

        except UnicodeDecodeError:

            invalid += 1

            problems.append({
                "file": str(file),
                "severity": "error",
                "message": "Encodage UTF-8 invalide."
            })

    if invalid == 0:
        return 2

    ratio = 1 - (invalid / len(files))

    return max(0, round(ratio * 2))
def check_line_length(files, problems):
    """
    Vérifie que les lignes ne dépassent pas 120 caractères.
    """

    total = 0
    long_lines = 0

    for file in files:

        for number, line in enumerate(
            file.read_text(
                encoding="utf-8",
                errors="ignore"
            ).splitlines(),
            start=1
        ):

            total += 1

            if len(line) > 120:

                long_lines += 1

                problems.append({
                    "file": str(file),
                    "severity": "warning",
                    "message": f"Ligne {number} supérieure à 120 caractères."
                })

    if total == 0:
        return 3

    ratio = 1 - (long_lines / total)

    return max(0, round(ratio * 3))
def check_trailing_spaces(files, problems):
    """
    Vérifie les espaces en fin de ligne.
    """

    total = 0
    errors = 0

    for file in files:

        for number, line in enumerate(
            file.read_text(
                encoding="utf-8",
                errors="ignore"
            ).splitlines(),
            start=1
        ):

            total += 1

            if line.endswith(" "):

                errors += 1

                problems.append({
                    "file": str(file),
                    "severity": "warning",
                    "message": f"Espace inutile ligne {number}."
                })

    if total == 0:
        return 2

    ratio = 1 - (errors / total)

    return max(0, round(ratio * 2))
def check_code_blocks(files, problems):
    """
    Vérifie que tous les blocs ``` sont fermés.
    """

    errors = 0

    for file in files:

        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        fences = content.count("```")

        if fences % 2 != 0:

            errors += 1

            problems.append({
                "file": str(file),
                "severity": "error",
                "message": "Bloc de code Markdown non fermé."
            })

    if errors == 0:
        return 3

    ratio = 1 - (errors / len(files))

    return max(0, round(ratio * 3))
def check_code_blocks(files, problems):
    """
    Vérifie que tous les blocs ``` sont fermés.
    """

    errors = 0

    for file in files:

        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        fences = content.count("```")

        if fences % 2 != 0:

            errors += 1

            problems.append({
                "file": str(file),
                "severity": "error",
                "message": "Bloc de code Markdown non fermé."
            })

    if errors == 0:
        return 3

    ratio = 1 - (errors / len(files))

    return max(0, round(ratio * 3))
def check_lists(files, problems):
    """
    Les listes sont déjà vérifiées par markdownlint.
    """

    return 2
def check_tables(files, problems):
    """
    Les tableaux sont vérifiés par markdownlint.
    """

    return 2
import re

HTML_TAGS = (
    "font",
    "center",
    "marquee"
)


def check_html(files, problems):

    errors = 0

    for file in files:

        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        for tag in HTML_TAGS:

            if re.search(fr"<{tag}\b", content):

                errors += 1

                problems.append({
                    "file": str(file),
                    "severity": "warning",
                    "message": f"Balise HTML <{tag}> déconseillée."
                })

    if errors == 0:
        return 3

    ratio = 1 - (errors / len(files))

    return max(0, round(ratio * 3))
