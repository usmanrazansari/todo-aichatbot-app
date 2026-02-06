from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session
from typing import List
from ..db.database import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from ..services.task_service import (
    get_tasks_by_user_id,
    get_task_by_id_and_user,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)
from ..utils.jwt_handler import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json


router = APIRouter()
security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user ID from the JWT token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        User ID as string
    """
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user_id


@router.get("/tasks", response_model=List[TaskPublic])
def list_tasks(
    user_id: str = Path(..., description="The ID of the user whose tasks to retrieve"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        List of tasks for the user
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID in path does not match authenticated user"
        )

    tasks = get_tasks_by_user_id(session, user_id)
    return tasks


@router.post("/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    user_id: str = Path(..., description="The ID of the user to create the task for"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for a specific user.

    Args:
        task_data: Task creation data
        user_id: The ID of the user to create the task for
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        Created task object
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID in path does not match authenticated user"
        )

    # Validate that title is not empty
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    task = create_task(session, task_data, user_id)
    return task


@router.get("/tasks/{id}", response_model=TaskPublic)
def get_task(
    id: str = Path(..., description="The ID of the task to retrieve"),
    user_id: str = Path(..., description="The ID of the user"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task for a user.

    Args:
        id: The ID of the task to retrieve
        user_id: The ID of the user
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        Task object
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID in path does not match authenticated user"
        )

    task = get_task_by_id_and_user(session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{id}", response_model=TaskPublic)
def update_existing_task(
    task_data: TaskUpdate,
    id: str = Path(..., description="The ID of the task to update"),
    user_id: str = Path(..., description="The ID of the user"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for a user.

    Args:
        id: The ID of the task to update
        task_data: Task update data
        user_id: The ID of the user
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        Updated task object
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID in path does not match authenticated user"
        )

    # Validate that if title is provided, it's not empty
    if task_data.title is not None and not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    updated_task = update_task(session, id, user_id, task_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    id: str = Path(..., description="The ID of the task to delete"),
    user_id: str = Path(..., description="The ID of the user"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for a user.

    Args:
        id: The ID of the task to delete
        user_id: The ID of the user
        current_user_id: The ID of the currently authenticated user
        session: Database session
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID in path does not match authenticated user"
        )

    deleted = delete_task(session, id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/tasks/{id}/complete", response_model=TaskPublic)
def toggle_task_completion_status(
    id: str = Path(..., description="The ID of the task to update"),
    user_id: str = Path(..., description="The ID of the user"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.

    Args:
        id: The ID of the task to update
        user_id: The ID of the user
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        Updated task object with new completion status
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user ID in path does not match authenticated user"
        )

    updated_task = toggle_task_completion(session, id, user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task