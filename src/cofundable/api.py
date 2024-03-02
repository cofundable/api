"""Instantiate the Cofundable API and root-level endpoints."""

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from cofundable.routers.bookmarks import bookmark_router
from cofundable.routers.causes import cause_router
from cofundable.routers.users import user_router

app = FastAPI()
app.include_router(cause_router)
app.include_router(user_router)
app.include_router(bookmark_router)
add_pagination(app)


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
