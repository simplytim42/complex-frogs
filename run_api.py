"""Main API file for Complex Frogs API."""

from fastapi import FastAPI, status

from complex_frogs.api import scrape_data, targets
from complex_frogs.logger.config import LOGS_DIR, setup_logger

setup_logger(LOGS_DIR / "api.log")

app = FastAPI()
app.include_router(targets.router)
app.include_router(scrape_data.router)


@app.get(
    "/",
    status_code=status.HTTP_418_IM_A_TEAPOT,
    response_description="Generic Message. Used to confirm API is running.",
)
def root() -> dict[str, str]:
    """Root endpoint for API."""
    return {"message": "Complex Frogs API"}
