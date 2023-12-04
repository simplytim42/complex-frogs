from pathlib import Path

from sqlalchemy import create_engine

from .models import Base

root_dir = Path(__file__).resolve().parent.parent.parent
db_location = root_dir / "frog.db"
engine = create_engine(f"sqlite:////{db_location}")

Base.metadata.create_all(bind=engine, checkfirst=True)
