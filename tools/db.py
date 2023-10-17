from pathlib import Path
from datetime import date
import logging


class Database:
    db_name = "products.txt"

    def __init__(self):
        self.db = Path(__file__).resolve().parent.parent / self.db_name
        if not self.db.exists():
            self.db.touch()
            logging.debug(f"Created database {self.db_name}")

    def add_record(self, *args):
        today = date.today().isoformat()
        values = today, *args
        record = "|".join(values) + "\n"
        logging.debug(f"Preparing to add record: |||{record.strip()}|||")

        if not self._record_exists(record):
            with self.db.open("a") as f:
                f.write(record)
                logging.info(f"Added record: |||{record.strip()}|||")

    def _record_exists(self, record):
        return record in self.db.read_text()
