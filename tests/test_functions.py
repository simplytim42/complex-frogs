from tools.functions import write_file
from tempfile import TemporaryDirectory
from pathlib import Path


def test_write_file():
    with TemporaryDirectory() as tmp_dir:
        file = write_file(dir=Path(tmp_dir), filename="test.txt", content="test")
        assert file.exists()
        assert file.read_text() == "test"
