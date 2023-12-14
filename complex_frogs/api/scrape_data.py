"""API endpoints for scraped data."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from complex_frogs.database import crud, get_db, schema

router = APIRouter(
    prefix="/scrape-data",
    tags=["scrape data"],
)


@router.get(
    "/",
    response_model=list[schema.ScrapeDataOut],
    response_description="A list of all Scrape Data!",
)
def get_scrape_data(session: Annotated[Session, Depends(get_db)]) -> Any:
    """Get all Scrape Data from database."""
    try:
        scraped_data = crud.read_scrape_data(session)
    except SQLAlchemyError as e:
        logging.exception(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        logging.info("Getting all scrape data from database")
        return scraped_data


@router.get(
    "/target/{target_id}",
    response_model=list[schema.ScrapeDataOut],
    response_description="A list of all Scrape Data for the specified Target",
)
def get_scrape_data_for_target(
    target_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Get all Scrape Data for a specific Target from database."""
    try:
        scraped_data = crud.read_scrape_data_for_target(session, target_id)
    except crud.TargetDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found",
        ) from None
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        ) from None
    else:
        msg = f"Getting all scrape data for target with id {target_id} from database"
        logging.info(msg=msg)
        return scraped_data


@router.get(
    "/{scrape_data_id}",
    response_model=schema.ScrapeDataOut,
    response_description="The specified Scrape Data",
)
def get_scrape_data_by_id(
    scrape_data_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Get specific Scrape Data by ID from database."""
    try:
        scraped_data = crud.read_scrape_data_by_id(session, scrape_data_id)
    except crud.ScrapedDataDoesNotExistError:
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
        msg = f"Getting scrape data with id {scrape_data_id} from database"
        logging.info(msg=msg)
        return scraped_data


@router.delete(
    "/{scrape_data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="No content",
)
def delete_scrape_data(
    scrape_data_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete specific Scrape Data from the database."""
    try:
        crud.delete_scrape_data(session, scrape_data_id)
    except crud.ScrapedDataDoesNotExistError:
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
        msg = f"Deleted scrape data with id {scrape_data_id} from database"
        logging.info(msg=msg)
