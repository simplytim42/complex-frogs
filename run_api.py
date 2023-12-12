"""Main API file for Complex Frogs API."""

import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from complex_frogs.database import crud, engine, models, schema
from complex_frogs.logger.config import LOGS_DIR, setup_logger

setup_logger(LOGS_DIR / "api.log")

app = FastAPI()
session = Session(engine)


class Tags(Enum):
    """Tags for endpoints."""

    targets = "targets"
    scrape_data = "scraped data"


@app.get(
    "/",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    response_description="Generic Message. Used to confirm API is running.",
)
def root() -> dict[str, str]:
    """Root endpoint for API."""
    return {"message": "Complex Frogs API"}


@app.get(
    "/targets",
    response_model=list[schema.Target],
    tags=[Tags.targets],
    response_description="A list of all Scraping Targets",
)
def get_targets() -> Any:
    """Get all Scraping Targets from the database."""
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


@app.get(
    "/targets/{target_id}",
    response_model=schema.Target,
    tags=[Tags.targets],
    response_description="The requested Scraping Target",
)
def get_target(target_id: int) -> Any:
    """Get a single Scraping Target from database."""
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


@app.post(
    "/targets",
    response_model=schema.NewTarget,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.targets],
    response_description="The newly created Scraping Target",
)
def new_target(new_target: schema.NewTarget) -> Any:
    """Create a new Scraping Target in the database."""
    try:
        msg = f"Creating new target with sku '{new_target.sku}' in database"
        logging.info(msg=msg)
        now = datetime.now(tz=timezone.utc)
        last = datetime(1970, 1, 1, tzinfo=timezone.utc)
        target = models.ScrapeTargets(
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


@app.put(
    "/targets/{target_id}",
    response_model=schema.NewTarget,
    tags=[Tags.targets],
    response_description="The updated Scraping Target",
)
def update_target(target_id: int, new_target: schema.NewTarget) -> Any:
    """Update a Scraping Target in the database."""
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


@app.delete(
    "/targets/{target_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[Tags.targets],
    response_description="No content",
)
def delete_target(target_id: int) -> None:
    """Delete a Scraping Target from the database."""
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


@app.get(
    "/scrape-data",
    response_model=list[schema.ScrapeResult],
    tags=[Tags.scrape_data],
    response_description="A list of all Scrape Data!",
)
def get_scrape_data() -> Any:
    """Get all Scrape Data from database."""
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


@app.get(
    "/scrape-data/target/{target_id}",
    response_model=list[schema.ScrapeResult],
    tags=[Tags.scrape_data],
    response_description="A list of all Scrape Data for the specified Target",
)
def get_scrape_data_for_target(target_id: int) -> Any:
    """Get all Scrape Data for a specific Target from database."""
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


@app.get(
    "/scrape-data/{scrape_data_id}",
    response_model=schema.ScrapeResult,
    tags=[Tags.scrape_data],
    response_description="The specified Scrape Data",
)
def get_scrape_data_by_id(scrape_data_id: int) -> Any:
    """Get specific Scrape Data by ID from database."""
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


@app.delete(
    "/scrape-data/{scrape_data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[Tags.scrape_data],
    response_description="No content",
)
def delete_scrape_data(scrape_data_id: int) -> None:
    """Delete specific Scrape Data from the database."""
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
