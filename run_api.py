"""Main API file for Complex Frogs API."""

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from complex_frogs.database import crud, engine
from complex_frogs.database.models import ScrapeTargets
from complex_frogs.logger.config import LOGS_DIR, setup_logger
from complex_frogs.models.scraper import NewTarget, ScrapeResult, Target

setup_logger(LOGS_DIR / "api.log")

app = FastAPI()
session = Session(engine)


@app.get("/", status_code=status.HTTP_418_IM_A_TEAPOT)
def root() -> dict[str, str]:
    """Root endpoint for API."""
    logging.info("Root endpoint hit")
    return {"message": "Complex Frogs API"}


@app.get("/targets", response_model=list[Target])
def get_targets() -> Any:
    """Get all scraping targets from database."""
    try:
        logging.info("Getting all targets from database")
        targets = crud.read_targets(session)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return targets


@app.get("/targets/{target_id}", response_model=Target)
def get_target(target_id: int) -> Any:
    """Get a single scraping target from database."""
    try:
        msg = f"Getting target with id {target_id} from database"
        logging.info(msg=msg)
        target = crud.read_target(session, target_id)
        if target is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target not found",
            )
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return target


@app.post("/targets", response_model=NewTarget, status_code=status.HTTP_201_CREATED)
def new_target(new_target: NewTarget) -> Any:
    """Create a new scraping target in the database."""
    try:
        msg = f"Creating new target with sku '{new_target.sku}' in database"
        logging.info(msg=msg)
        now = datetime.now(tz=timezone.utc)
        last = datetime(1970, 1, 1, tzinfo=timezone.utc)
        target = ScrapeTargets(
            **new_target.model_dump(),
            date_added=now,
            last_scraped=last,
        )
        created_target = crud.create_target(session, target)
    except crud.TargetExistsError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Target already exists",
        ) from None
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return created_target


@app.put("/targets/{target_id}", response_model=NewTarget)
def update_target(target_id: int, new_target: NewTarget) -> Any:
    """Update a scraping target in the database."""
    try:
        msg = f"Updating target with id {target_id} in database"
        logging.info(msg=msg)
        target = crud.update_target(session, target_id, new_target)
    except crud.TargetDoesNotExistError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        ) from None
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return target


@app.delete("/targets/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_target(target_id: int):
    """Delete a scraping target from the database."""
    try:
        msg = f"Deleting target with id {target_id} from database"
        logging.info(msg=msg)
        crud.delete_target(session, target_id)
    except crud.TargetDoesNotExistError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        ) from None
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None


@app.get("/scrape-data", response_model=list[ScrapeResult])
def get_scrape_data() -> Any:
    """Get all scrape data from database."""
    try:
        logging.info("Getting all scrape data from database")
        scraped_data = crud.read_scrape_data(session)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return scraped_data


@app.get("/scrape-data/target/{target_id}", response_model=list[ScrapeResult])
def get_scrape_data_for_target(target_id: int) -> Any:
    """Get all scrape data for a target from database."""
    try:
        msg = f"Getting all scrape data for target with id {target_id} from database"
        logging.info(msg=msg)
        scraped_data = crud.read_scrape_data_for_target(session, target_id)
    except crud.TargetDoesNotExistError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        ) from None
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return scraped_data


@app.get("/scrape-data/{scrape_data_id}", response_model=ScrapeResult)
def get_scrape_data_by_id(scrape_data_id: int) -> Any:
    """Get specific scrape data by id from database."""
    try:
        msg = f"Getting scrape data with id {scrape_data_id} from database"
        logging.info(msg=msg)
        scraped_data = crud.read_scrape_data_by_id(session, scrape_data_id)
    except crud.ScrapedDataDoesNotExistError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scrape data not found",
        ) from None
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        return scraped_data


@app.delete("/scrape-data/{scrape_data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scrape_data(scrape_data_id: int):
    """Delete individual scrape data from the database."""
    try:
        msg = f"Deleting scrape data with id {scrape_data_id} from database"
        logging.info(msg=msg)
        crud.delete_scrape_data(session, scrape_data_id)
    except crud.ScrapedDataDoesNotExistError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scrape data not found",
        ) from None
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None


session.close()
