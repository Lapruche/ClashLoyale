import re
from pathlib import Path


def path_number(path: Path) -> int:
    match = re.search(r"\d+", path.stem)  # Regex that gets the index in the file name
    return int(match.group()) if match else 0
