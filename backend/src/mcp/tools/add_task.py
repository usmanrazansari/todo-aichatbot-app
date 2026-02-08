"""
MCP Tool: add_task

Adds a new task to the user's todo list.
"""

from sqlmodel import Session
from src.services.task_service import create_task
from src.models.task import TaskCreate
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def add_task_tool(
    title: str,
    user_id: str,
    description: str = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Add a new task to the user's todo list.

    Args:
        title: Task title (required)
        user_id: User ID (required)
        description: Task description (optional)
        session: Database session (injected by handler)

    Returns:
        Dictionary with success status and task details or error message
    """
    try:
        # Create task data
        task_data = TaskCreate(
            title=title,
            description=description
        )

        # Create task using existing service
        task = create_task(session, task_data, user_id)

        logger.info(f"MCP tool add_task: Created task {task.id} for user {user_id}")

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
        }

    except Exception as e:
        error_msg = f"Failed to create task: {str(e)}"
        logger.error(f"MCP tool add_task error: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


# Tool schema for OpenAI function calling
ADD_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The title or name of the task. Should be concise and descriptive."
        },
        "description": {
            "type": "string",
            "description": "Optional detailed description or notes about the task."
        }
    },
    "required": ["title"],
    "additionalProperties": False
}
