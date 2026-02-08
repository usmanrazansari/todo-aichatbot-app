"""
MCP Tool: complete_task

Marks a task as completed.
"""

from sqlmodel import Session
from src.services.task_service import toggle_task_completion, get_task_by_id_and_user
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def complete_task_tool(
    task_id: str,
    user_id: str,
    session: Session = None
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        task_id: Task ID (required)
        user_id: User ID (required, for authorization)
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

        # Toggle task completion (will set to completed if not already)
        updated_task = toggle_task_completion(session, task_id, user_id)

        if not updated_task:
            return {
                "success": False,
                "error": "Failed to complete task"
            }

        # Ensure task is marked as completed
        if not updated_task.completed:
            # If it was already completed and got toggled back, toggle again
            updated_task = toggle_task_completion(session, task_id, user_id)

        logger.info(f"MCP tool complete_task: Completed task {task_id} for user {user_id}")

        return {
            "success": True,
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "completed": updated_task.completed,
                "updated_at": updated_task.updated_at.isoformat()
            }
        }

    except Exception as e:
        error_msg = f"Failed to complete task: {str(e)}"
        logger.error(f"MCP tool complete_task error: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


# Tool schema for OpenAI function calling
COMPLETE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {
            "type": "string",
            "description": "The ID of the task to mark as completed"
        },
        "user_id": {
            "type": "string",
            "description": "The ID of the user who owns this task"
        }
    },
    "required": ["task_id", "user_id"],
    "additionalProperties": False
}
