from pathlib import Path
from datetime import date


class Database:
    def __init__(self):
        self.db = Path("products.txt")
        if not self.db.exists():
            self.db.touch()

    def add_record(self, *args):
        today = date.today().isoformat()
        values = today, *args
        record = "|".join(values) + "\n"

        if not self._record_exists(record):
            with self.db.open("a") as f:
                f.write(record)

    def _record_exists(self, record):
        return record in self.db.read_text()
