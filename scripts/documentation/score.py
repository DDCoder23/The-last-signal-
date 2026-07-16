from .markdown import check_markdown
from .titles import check_titles
from .spelling import check_spelling
from .links import check_links
from .python_docs import check_python_docs
from .rust_docs import check_rust_docs
from .organization import check_organization
from .navigation import check_navigation
from .report import generate_report
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
    all_problems = []

    for name, check in checks.items():
        try:
            result = check()
            assert (result is Dict)
        except Exception as e:
            result={
            "score": 0,
            "max_score": 0,
            "results": {},
            "problems": [{
                "file": "",
                "severity": "error",
                "message": f"Erreur:{str(e)}"
            }]}
        finally:
            scores[name] = result["score"]
            details[name] = result
            for problem in result["problems"]:
                problem["module"] = name

            all_problems.extend(result["problems"])

    

    total = sum(scores.values())
    generate_report(total,scores,details,all_problems)
    
    return total
