def generate_score():

    scores = {}
    details = {}

    markdown = check_markdown()

    scores["markdown"] = markdown["score"]
    details["markdown"] = markdown

    scores["titles"] = check_titles()
    scores["spelling"] = check_spelling()
    scores["links"] = check_links()
    scores["python"] = check_python_docs()
    scores["rust"] = check_rust_docs()
    scores["organization"] = check_organization()
    scores["navigation"] = check_navigation()

    total = sum(scores.values())

    generate_report(
        total,
        scores,
        details
    )

    return total
