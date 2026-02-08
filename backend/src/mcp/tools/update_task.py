"""
MCP Tool: update_task

Updates an existing task's title, description, or completion status.
"""

from sqlmodel import Session
from src.services.task_service import update_task as update_task_service, get_task_by_id_and_user
from src.models.task import TaskUpdate
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def update_task_tool(
    task_id: str,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Update an existing task's details.

    Args:
        task_id: Task ID (required)
        user_id: User ID (required, for authorization)
        title: New task title (optional)
        description: New task description (optional)
        completed: New completion status (optional)
        session: Database session (injected by handler)

    Returns:
        Dictionary with success status and updated task details or error message
    """
    try:
        # Verify task exists and user owns it
        existing_task = get_task_by_id_and_user(session, task_id, user_id)
        if not existing_task:
            return {
                "success": False,
                "error": "Task not found or access denied"
            }

        # Create update data
        update_data = TaskUpdate(
            title=title,
            description=description,
            completed=completed
        )

        # Update task using existing service (correct parameter order)
        updated_task = update_task_service(session, task_id, user_id, update_data)

        if not updated_task:
            return {
                "success": False,
                "error": "Failed to update task"
            }

        logger.info(f"MCP tool update_task: Updated task {task_id} for user {user_id}")

        return {
            "success": True,
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description,
                "completed": updated_task.completed,
                "updated_at": updated_task.updated_at.isoformat()
            }
        }

    except Exception as e:
        error_msg = f"Failed to update task: {str(e)}"
        logger.error(f"MCP tool update_task error: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


# Tool schema for OpenAI function calling
UPDATE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {
            "type": "string",
            "description": "The ID of the task to update"
        },
        "title": {
            "type": "string",
            "description": "New task title (optional)"
        },
        "description": {
            "type": "string",
            "description": "New task description (optional)"
        },
        "completed": {
            "type": "boolean",
            "description": "New completion status (optional)"
        }
    },
    "required": ["task_id"],
    "additionalProperties": False
}
