"""API endpoints for scraped data."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import crud, get_db, schema

router = APIRouter(
    prefix="/scrape-data",
    tags=["Scrape Data"],
)


@router.get(
    "/",
    response_model=list[schema.ScrapeDataOut],
    response_description="A list of all Scrape Data!",
)
def get_scrape_data(session: Annotated[Session, Depends(get_db)]) -> Any:
    """Get all Scrape Data from database."""
    scraped_data = crud.read_scrape_data(session)
    logging.info("Getting all scrape data from database")
    return scraped_data


@router.get(
    "/target/{target_id}",
    response_model=list[schema.ScrapeDataOut],
    response_description="A list of all Scrape Data for the specified Target",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": schema.TargetDoesNotExistMessage,
        },
    },
)
def get_scrape_data_for_target(
    target_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Get all Scrape Data for a specific Target from database."""
    scraped_data = crud.read_scrape_data_for_target(session, target_id)
    msg = f"Getting all scrape data for target with id {target_id} from database"
    logging.info(msg=msg)
    return scraped_data


@router.get(
    "/{scrape_data_id}",
    response_model=schema.ScrapeDataOut,
    response_description="The specified Scrape Data",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": schema.ScrapeDataDoesNotExistMessage,
        },
    },
)
def get_scrape_data_by_id(
    scrape_data_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Get specific Scrape Data by ID from database."""
    scraped_data = crud.read_scrape_data_by_id(session, scrape_data_id)
    msg = f"Getting scrape data with id {scrape_data_id} from database"
    logging.info(msg=msg)
    return scraped_data


@router.delete(
    "/{scrape_data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="No content",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": schema.ScrapeDataDoesNotExistMessage,
        },
    },
)
def delete_scrape_data(
    scrape_data_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete specific Scrape Data from the database."""
    crud.delete_scrape_data(session, scrape_data_id)
    msg = f"Deleted scrape data with id {scrape_data_id} from database"
    logging.info(msg=msg)
