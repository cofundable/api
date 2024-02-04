"""Instantiate the Cofundable API and root-level endpoints."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    """Welcome user to the API and direct to openAPI spec."""
    return {
        "status": "ok",
        "message": (
            "Welcome to the Cofundable API. "
            "Visit /docs for more information about the API resources available."
        ),
    }


@app.get("/health-check")
async def health_check() -> dict:
    """Check that the API is available."""
    return {"status": "ok"}
