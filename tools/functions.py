"""General functions for the app."""

import logging
from datetime import datetime, timezone
from pathlib import Path


def write_file(directory: Path, filename: str, content: str) -> Path:
    """Write a file to a directory and return the path to the file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filepath = directory / f"{timestamp}_{filename}"
    with Path(__file__).resolve().parent / filepath as file:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
        msg = f"writing file to '{file.name}'"
        logging.info(msg=msg)
        return file
