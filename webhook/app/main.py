"""
Main entry point for the webhook service.
"""

import logging
import sys
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .api import router
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Observatory Webhook Service",
    description="Webhook service for the Observatory monitoring stack",
    version=__version__,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint.
    """
    return {
        "name": "Observatory Webhook Service",
        "version": __version__,
        "status": "running",
    }


if __name__ == "__main__":
    logger.info(f"Starting Observatory Webhook Service v{__version__}")
    logger.info(f"Debug mode: {settings.debug}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )