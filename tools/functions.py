from datetime import datetime
from pathlib import Path


def write_file(dir: Path, filename: str, content: str) -> Path:
    """Write a file to a directory and return the path to the file."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = dir / f"{timestamp}_{filename}"
    with Path(__file__).resolve().parent / filepath as file:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
        return file
