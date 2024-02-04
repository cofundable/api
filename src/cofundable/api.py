from fastapi import FastAPI

app = FastAPI()


@app.get("/health-check")
async def health_check():
    """Check that the API is available."""
    return {"status": "ok"}
