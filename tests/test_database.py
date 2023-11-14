from tools.database import Database
import pytest


@pytest.fixture
def database():
    database = Database("test.txt")
    yield database
    # teardown happens after the yield stmt
    database.db.unlink()


def test_db_init(database):
    assert database.db.exists()


def test_db_add_record(database):
    database.add_record("test")
    assert "test" in database.db.read_text()
