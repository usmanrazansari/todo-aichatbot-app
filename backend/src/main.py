from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import task_routes
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI app instance
app = FastAPI(title="Todo Application API", version="1.0.0")


# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(task_routes.router, prefix="/api/{user_id}", tags=["tasks"])


@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Todo Application API is running!"}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "todo-api"}


# Error handlers
@app.exception_handler(404)
async def not_found_error(request, exc):
    logger.warning(f"Not found error: {request.url}")
    return {"message": "Resource not found"}


@app.exception_handler(500)
async def server_error(request, exc):
    logger.error(f"Server error: {str(exc)}")
    return {"message": "Internal server error"}