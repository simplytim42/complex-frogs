"""Main API file for Complex Frogs API."""

import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from complex_frogs.database import engine
from complex_frogs.database.models import ScrapeTargets
from complex_frogs.models.scraper import Target

app = FastAPI()
session = Session(engine)


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint for API."""
    logging.info("Root endpoint hit")
    return {"message": "Complex Frogs API"}


@app.get("/targets")
def get_targets() -> list[Target]:
    """Get all scraping targets from database."""
    try:
        logging.info("Getting targets from database")
        stmt = select(ScrapeTargets)
        targets = session.scalars(stmt)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return targets  # type: ignore[return-value]


session.close()
