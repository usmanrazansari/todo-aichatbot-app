from sqlmodel import Session, select, update
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from fastapi import HTTPException, status
from datetime import datetime


def get_tasks_by_user_id(session: Session, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve

    Returns:
        List of tasks belonging to the user
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a specific task by its ID and user ID.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found and belongs to user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a user.

    Args:
        session: Database session
        task_data: Task creation data
        user_id: ID of the user creating the task

    Returns:
        Created Task object
    """
    task = Task(**task_data.model_dump(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task_id: str, user_id: str, task_data: TaskUpdate) -> Optional[Task]:
    """
    Update an existing task for a user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        task_data: Task update data

    Returns:
        Updated Task object if successful, None if task not found
    """
    # First, get the existing task to ensure it exists and belongs to the user
    existing_task = get_task_by_id_and_user(session, task_id, user_id)
    if not existing_task:
        return None

    # Prepare update data, excluding None values to allow partial updates
    update_data = task_data.model_dump(exclude_unset=True, exclude_none=True)

    # Update the task
    for field, value in update_data.items():
        setattr(existing_task, field, value)

    # Update the updated_at timestamp
    existing_task.updated_at = datetime.utcnow()

    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task


def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """
    Delete a task for a user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Returns:
        True if task was deleted, False if task not found
    """
    # First, get the existing task to ensure it exists and belongs to the user
    existing_task = get_task_by_id_and_user(session, task_id, user_id)
    if not existing_task:
        return False

    # Delete the task
    session.delete(existing_task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task

    Returns:
        Updated Task object if successful, None if task not found
    """
    # First, get the existing task to ensure it exists and belongs to the user
    existing_task = get_task_by_id_and_user(session, task_id, user_id)
    if not existing_task:
        return None

    # Toggle the completion status
    existing_task.completed = not existing_task.completed
    existing_task.updated_at = datetime.utcnow()

    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task