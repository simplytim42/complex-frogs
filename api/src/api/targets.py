"""API Endpoints for Scraping Targets."""

import logging
from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src import messages
from src.database import crud, get_db, models, schema

router = APIRouter(
    prefix="/targets",
    tags=["Targets"],
)


@router.get(
    "/",
    response_model=list[schema.TargetOut],
    response_description="A list of all Scraping Targets",
)
def get_targets(session: Annotated[Session, Depends(get_db)]) -> Any:
    """Get all Scraping Targets from the database."""
    targets = crud.read_targets(session)
    logging.info("Getting all targets from database")
    return targets


@router.post(
    "/",
    response_model=schema.TargetOut,
    status_code=status.HTTP_201_CREATED,
    response_description="The newly created Scraping Target",
    responses={
        status.HTTP_409_CONFLICT: {
            "model": messages.TargetExistsMessage,
        },
    },
)
def new_target(
    new_target: schema.TargetIn,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Create a new Scraping Target in the database.

    ## Usage Notes
    ### Amazon UK Target
    - `site` must be set to `amz`
    - `sku` must be set to the Amazon product ASIN

    ### Amazon UK via Google Shopping Target
    - `site` must be set to `amz-g`
    - `sku` must be set to the full name of the book as shown on Amazon UK. The closer the name is to the actual name on Amazon UK, the better the results will be.

    ### Go Outdoors Target
    - `site` must be set to `go_od`
    - `sku` must be set to the Product ID and name as set in the URL of the product page on Go Outdoors. For example, for the product at `https://www.gooutdoors.co.uk/15903050/family-tent-123456`, the `sku` would be `family-tent-123456`
    """
    now = datetime.now(tz=timezone.utc)
    last = datetime(1970, 1, 1, tzinfo=timezone.utc)
    target = models.ScrapeTargets(
        **new_target.model_dump(),
        date_added=now,
        last_scraped=last,
    )
    created_target = crud.create_target(session, target)

    msg = f"Created new target with sku '{new_target.sku}' in database"
    logging.info(msg=msg)
    return created_target


@router.get(
    "/{target_id}",
    response_model=schema.TargetOut,
    response_description="The requested Scraping Target",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": messages.TargetDoesNotExistMessage,
        },
    },
)
def get_target(
    target_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Get a single Scraping Target from database."""
    target = crud.read_target(session, target_id)

    if target is None:
        raise crud.TargetDoesNotExistError

    msg = f"Getting target with id {target_id} from database"
    logging.info(msg=msg)
    return target


@router.put(
    "/{target_id}",
    response_model=schema.TargetOut,
    response_description="The updated Scraping Target",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": messages.TargetDoesNotExistMessage,
        },
    },
)
def update_target(
    target_id: int,
    new_target: schema.TargetIn,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Update a Scraping Target in the database.

    See *Usage Notes* for `POST /targets/` for helpful details about updating Scraping Targets.
    """
    target = crud.update_target(session, target_id, new_target)
    msg = f"Updated target with id {target_id} in database"
    logging.info(msg=msg)
    return target


@router.delete(
    "/{target_id}",
    response_model=schema.TargetOut,
    response_description="No content",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": messages.TargetDoesNotExistMessage,
        },
    },
)
def delete_target(
    target_id: int,
    session: Annotated[Session, Depends(get_db)],
) -> Any:
    """Delete a Scraping Target from the database."""
    deleted_target = crud.delete_target(session, target_id)
    msg = f"Deleted target with id {target_id} from database"
    logging.info(msg=msg)
    return deleted_target
