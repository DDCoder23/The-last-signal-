def generate_score():
    checks = {
    "markdown": check_markdown,
    "titles": check_titles,
    "spelling": check_spelling,
    "links": check_links,
    "python": check_python_docs,
    "rust": check_rust_docs,
    "organization": check_organization,
    "navigation": check_navigation,
}

    scores = {}
    details = {}

    for name, check in checks.items():
        result = check()
        scores[name] = result["score"]
        details[name] = result

    total = sum(scores.values())
    with open ():
