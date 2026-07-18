import re
from pathlib import Path


def read_report(path):

    path = Path(path)

    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def extract_int(pattern, text, default=0):

    match = re.search(pattern, text)

    if match:
        return int(match.group(1))

    return default


def extract_float(pattern, text, default=0):

    match = re.search(pattern, text)

    if match:
        return float(match.group(1))

    return default
