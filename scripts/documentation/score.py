from documentation.markdown import check_markdown
from documentation.titles import check_titles
from documentation.spelling import check_spelling
from documentation.links import check_links
from documentation.python_docs import check_python_docs
from documentation.rust_docs import check_rust_docs
from documentation.organization import check_organization
from documentation.navigation import check_navigation

from documentation.report import generate_report


def generate_score():
    scores = {}

    scores["markdown"] = check_markdown()
    scores["titles"] = check_titles()
    scores["spelling"] = check_spelling()
    scores["links"] = check_links()
    scores["python"] = check_python_docs()
    scores["rust"] = check_rust_docs()
    scores["organization"] = check_organization()
    scores["navigation"] = check_navigation()

    total = sum(scores.values())

    generate_report(total, scores)

    return total
