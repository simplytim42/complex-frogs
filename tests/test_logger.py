from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from complex_frogs.logger.config import setup_logger


def test_setup_logger():
    with TemporaryDirectory() as td, NamedTemporaryFile(dir=td) as t:
        filepath = Path(t.name)
        setup_logger(filepath=filepath)

        assert filepath.exists()
