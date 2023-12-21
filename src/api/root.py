"""Root API endpoints."""

from fastapi import APIRouter, status

from src import messages

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    response_description="Generic Message. Used to confirm API is running.",
)
def root() -> dict[str, str]:
    """Root endpoint for API."""
    return messages.RootMessage().model_dump()
