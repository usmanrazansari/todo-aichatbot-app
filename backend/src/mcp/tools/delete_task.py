"""
MCP Tool: delete_task

Permanently deletes a task from the user's list.
"""

from sqlmodel import Session
from src.services.task_service import delete_task as delete_task_service, get_task_by_id_and_user
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def delete_task_tool(
    task_id: str,
    user_id: str,
    session: Session = None
) -> Dict[str, Any]:
    """
    Permanently delete a task from the user's list.

    Args:
        task_id: Task ID (required)
        user_id: User ID (required, for authorization)
        session: Database session (injected by handler)

    Returns:
        Dictionary with success status and confirmation message or error message
    """
    try:
        # Verify task exists and user owns it
        existing_task = get_task_by_id_and_user(session, task_id, user_id)
        if not existing_task:
            return {
                "success": False,
                "error": "Task not found or access denied"
            }

        # Store task title for confirmation message
        task_title = existing_task.title

        # Delete task using existing service
        success = delete_task_service(session, task_id, user_id)

        if not success:
            return {
                "success": False,
                "error": "Failed to delete task"
            }

        logger.info(f"MCP tool delete_task: Deleted task {task_id} for user {user_id}")

        return {
            "success": True,
            "message": f"Task '{task_title}' deleted successfully"
        }

    except Exception as e:
        error_msg = f"Failed to delete task: {str(e)}"
        logger.error(f"MCP tool delete_task error: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


# Tool schema for OpenAI function calling
DELETE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {
            "type": "string",
            "description": "The ID of the task to delete"
        }
    },
    "required": ["task_id"],
    "additionalProperties": False
}
