from pathlib import Path

from sqlalchemy import create_engine

from .models import Base

db_location = Path(__file__).resolve().parent.parent / "frog.db"
engine = create_engine(f"sqlite:////{db_location}")

Base.metadata.create_all(bind=engine, checkfirst=True)
