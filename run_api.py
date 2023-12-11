"""Main API file for Complex Frogs API."""

import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from complex_frogs.database import engine
from complex_frogs.database.crud import read_target, read_targets
from complex_frogs.database.models import ScrapedData, ScrapeTargets
from complex_frogs.logger.config import LOGS_DIR, setup_logger
from complex_frogs.models.scraper import NewTarget, ScrapeResult, Target

setup_logger(LOGS_DIR / "api.log")

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
        logging.info("Getting all targets from database")
        targets = read_targets(session)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return targets  # type: ignore[return-value]


@app.get("/targets/{target_id}")
def get_target(target_id: int) -> Target:
    """Get a single scraping target from database."""
    try:
        msg = f"Getting target with id {target_id} from database"
        logging.info(msg=msg)
        target = read_target(session, target_id)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        if target is None:
            raise HTTPException(status_code=404, detail="Target not found")
        return target  # type: ignore[return-value]


@app.post("/targets")
def create_target(new_target: NewTarget) -> NewTarget:
    """Create a new scraping target in the database."""
    try:
        msg = f"Creating new target with sku '{new_target.sku}' in database"
        logging.info(msg=msg)
        now = datetime.now(tz=timezone.utc)
        stmt = ScrapeTargets(
            site=new_target.site,
            sku=new_target.sku,
            send_notification=new_target.send_notification,
            date_added=now,
            last_scraped=datetime(1970, 1, 1, tzinfo=timezone.utc),
        )
        session.add(stmt)
        session.commit()
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return new_target


@app.put("/targets/{target_id}")
def update_target(target_id: int, new_target: NewTarget) -> NewTarget:
    """Update a scraping target in the database."""
    try:
        msg = f"Updating target with id {target_id} in database"
        logging.info(msg=msg)
        target = read_target(session, target_id)

        if not target:
            raise HTTPException(status_code=404, detail="Target not found")

        target.site = new_target.site
        target.sku = new_target.sku
        target.send_notification = new_target.send_notification
        session.commit()
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return new_target


@app.delete("/targets/{target_id}")
def delete_target(target_id: int) -> dict[str, str]:
    """Delete a scraping target from the database."""
    try:
        msg = f"Deleting target with id {target_id} from database"
        logging.info(msg=msg)
        target = read_target(session, target_id)
        session.delete(target)
        session.commit()
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return {"message": f"Target with id {target_id} deleted"}


@app.get("/scrape-data")
def get_scrape_data() -> list[ScrapeResult]:
    """Get all scrape data from database."""
    try:
        logging.info("Getting all scrape data from database")
        stmt = select(ScrapedData)
        scraped_data = session.scalars(stmt)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return scraped_data  # type: ignore[return-value]


@app.get("/scrape-data/target/{target_id}")
def get_scrape_data_for_target(target_id: int) -> list[ScrapeResult]:
    """Get all scrape data for a target from database."""
    try:
        msg = f"Getting all scrape data for target with id {target_id} from database"
        logging.info(msg=msg)
        stmt = select(ScrapedData).where(ScrapedData.scrape_target_id == target_id)
        scraped_data = session.scalars(stmt)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return scraped_data  # type: ignore[return-value]


@app.delete("/scrape-data/{scrape_data_id}")
def delete_scrape_data(scrape_data_id: int) -> dict[str, str]:
    """Delete individual scrape data from the database."""
    try:
        msg = f"Deleting scrape data with id {scrape_data_id} from database"
        logging.info(msg=msg)
        stmt = select(ScrapedData).where(ScrapedData.id == scrape_data_id)
        scrape_data = session.scalar(stmt)
        session.delete(scrape_data)
        session.commit()
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(status_code=500, detail="Database error") from None
    else:
        return {"message": f"Scrape data with id {scrape_data_id} deleted"}


session.close()
