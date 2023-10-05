from pathlib import Path
from datetime import date


class FileDatabase:
    def __init__(self):
        self.db = Path("products.txt")
        if not self.db.exists():
            self.db.touch()

    def write_line(self, *args):
        args = date.today().isoformat(), *args
        with self.db.open("a") as f:
            f.write("|".join(args) + "\n")
