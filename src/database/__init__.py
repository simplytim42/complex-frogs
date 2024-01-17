from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base

root_dir = Path(__file__).resolve().parent.parent.parent
db_location = root_dir / "intrepid.db"
engine = create_engine(f"sqlite:////{db_location}")

Base.metadata.create_all(bind=engine, checkfirst=True)


def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    try:
        db = Session(engine)
        yield db
    finally:
        db.close()
