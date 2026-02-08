# Load environment variables from .env file FIRST (before any imports that need them)
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import task_routes, auth_routes, chat_routes
from src.db.database import engine
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from sqlmodel import SQLModel
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI app instance
app = FastAPI(title="Todo Application API", version="1.0.0")


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")


# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(auth_routes.router, prefix="/auth", tags=["authentication"])
app.include_router(task_routes.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(chat_routes.router, prefix="/api/{user_id}", tags=["chat"])


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
    from fastapi.responses import JSONResponse
    logger.warning(f"Not found error: {request.url}")
    return JSONResponse(status_code=404, content={"message": "Resource not found"})


@app.exception_handler(500)
async def server_error(request, exc):
    from fastapi.responses import JSONResponse
    logger.error(f"Server error: {str(exc)}")
    return JSONResponse(status_code=500, content={"message": "Internal server error"})