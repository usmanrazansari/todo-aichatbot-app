"""
MCP Tool: list_tasks

Retrieves all tasks for the user.
"""

from sqlmodel import Session
from src.services.task_service import get_tasks_by_user_id
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def list_tasks_tool(
    user_id: str,
    completed: Optional[bool] = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Retrieve all tasks for the user.

    Args:
        user_id: User ID (required)
        completed: Optional filter - true for completed only, false for pending only, None for all
        session: Database session (injected by handler)

    Returns:
        Dictionary with success status and list of tasks or error message
    """
    try:
        # Get tasks using existing service
        tasks = get_tasks_by_user_id(session, user_id)

        # Apply completed filter if specified
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        # Format tasks for response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

        logger.info(f"MCP tool list_tasks: Retrieved {len(task_list)} tasks for user {user_id}")

        return {
            "success": True,
            "tasks": task_list,
            "count": len(task_list)
        }

    except Exception as e:
        error_msg = f"Failed to retrieve tasks: {str(e)}"
        logger.error(f"MCP tool list_tasks error: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


# Tool schema for OpenAI function calling
LIST_TASKS_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "The ID of the user whose tasks to retrieve."
        },
        "completed": {
            "type": "boolean",
            "description": "Optional filter: true for completed tasks only, false for pending tasks only, omit for all tasks"
        }
    },
    "required": ["user_id"],
    "additionalProperties": False
}
