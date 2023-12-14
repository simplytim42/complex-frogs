"""Main API file for Complex Frogs API."""

from fastapi import FastAPI

from complex_frogs.api import root, scrape_data, targets
from complex_frogs.logger.config import LOGS_DIR, setup_logger

setup_logger(LOGS_DIR / "api.log")

app = FastAPI()
app.include_router(targets.router)
app.include_router(scrape_data.router)
app.include_router(root.router)
