"""Main API file for Complex Frogs API."""

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from complex_frogs.database import engine
from complex_frogs.database.models import ScrapeTargets
from complex_frogs.models.scraper import Target

LOGS_DIR = Path(__file__).parent / "logs"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=LOGS_DIR / "api.log",
)

app = FastAPI()
session = Session(engine)


@app.get("/")
def root():
    """Root endpoint for API."""
    return {"message": "Complex Frogs API"}


@app.get("/targets", response_model=list[Target])
def get_targets():
    """Get all scraping targets from database."""
    try:
        stmt = select(ScrapeTargets)
        targets = session.scalars(stmt)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return targets


session.close()
