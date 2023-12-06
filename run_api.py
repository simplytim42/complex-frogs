"""Main API file for Complex Frogs API."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Root endpoint for API."""
    return {"message": "Complex Frogs API"}
