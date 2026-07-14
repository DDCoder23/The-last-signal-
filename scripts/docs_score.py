import os
import json
from pathlib import Path
from datetime import datetime


REPORT_DIR = Path("reports/docs")

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def count_markdown_files():

    return len(
        list(Path(".").rglob("*.md"))
    )


def check_titles():

    files = list(Path(".").rglob("*.md"))

    if not files:
        return 0

    valid = 0

    for file in files:

        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        if "# " in content:

            valid += 1


    return int(
        (valid / len(files)) * 15
    )



def check_line_length():

    files = list(Path(".").rglob("*.md"))

    if not files:
        return 0


    total = 0
    errors = 0


    for file in files:

        for line in file.read_text(
            encoding="utf-8",
            errors="ignore"
        ).splitlines():

            total += 1

            if len(line) > 120:
                errors += 1


    if total == 0:
        return 10


    ratio = 1 - errors / total

    return max(
        0,
        int(ratio * 10)
    )



def check_python_docs():

    report = REPORT_DIR / "python-docs.md"

    if report.exists():

        return 15

    return 0



def check_rust_docs():

    if Path("Cargo.toml").exists():

        return 10

    return 0



def check_structure():

    required = [

        "README.md",
        "docs"

    ]

    score = 0


    if Path("README.md").exists():

        score += 5


    if Path("docs").exists():

        score += 5


    return score



def main():

    scores = {}


    scores["markdown"] = min(
        10,
        count_markdown_files()
    )


    scores["titles"] = check_titles()

    scores["line_length"] = check_line_length()


    # Ces valeurs seront remplacées
    # par les vrais rapports plus tard

    scores["spelling"] = 15

    scores["links"] = 15


    scores["python"] = check_python_docs()

    scores["rust"] = check_rust_docs()

    scores["organization"] = check_structure()



    total = sum(scores.values())


    data = {

        "date":
            datetime.now().isoformat(),

        "score":
            total,

        "details":
            scores

    }


    # score.txt utilisé par GitHub Actions

    (REPORT_DIR / "score.txt").write_text(
        str(total),
        encoding="utf-8"
    )


    (REPORT_DIR / "score.json").write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    markdown = f"""
# 📊 Documentation Score


## Score global

# {total}/100


## Détails


"""


    for key,value in scores.items():

        markdown += (
            f"- {key}: {value}\n"
        )


    (REPORT_DIR / "score.md").write_text(
        markdown,
        encoding="utf-8"
    )


    print(
        f"Documentation score : {total}/100"
    )



if __name__ == "__main__":

    main()
