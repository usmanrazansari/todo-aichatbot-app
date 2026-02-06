from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False


class Task(TaskBase, table=True):
    """
    Task model representing a todo item owned by a specific user.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)  # Indexed for efficient queries, no FK since Better Auth manages users
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """
    Model for creating new tasks.
    """
    pass


class TaskUpdate(SQLModel):
    """
    Model for updating existing tasks.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskPublic(TaskBase):
    """
    Public representation of a task (without internal fields).
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime