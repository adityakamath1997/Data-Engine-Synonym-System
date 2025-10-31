import logging
import sys

from fastapi import FastAPI

from app.api.routes import router

# Configure logging to stdout with color support
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI(
    title="Data Engine Synonym System",
    description="Synonym lookup API with Redis/Memory caching",
    version="1.0.0",
)

# Mount API routes under /api prefix
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok"}
