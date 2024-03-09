"""Logging configuration for the app."""

import logging
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"


def setup_logger(filepath: Path) -> None:
    """Start logger based on this config."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=filepath,
    )
