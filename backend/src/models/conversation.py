from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between user and AI assistant.

    A conversation contains multiple messages and persists across sessions.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique conversation identifier (UUID)"
    )

    user_id: str = Field(
        index=True,
        description="Owner of the conversation (from Better Auth JWT)"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the conversation was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the conversation was last updated"
    )

    title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional conversation title (auto-generated or user-set)"
    )

    archived: bool = Field(
        default=False,
        description="Soft delete flag for archived conversations"
    )


class ConversationCreate(SQLModel):
    """Model for creating new conversations."""
    title: Optional[str] = Field(default=None, max_length=255)


class ConversationUpdate(SQLModel):
    """Model for updating conversations."""
    title: Optional[str] = Field(default=None, max_length=255)
    archived: Optional[bool] = None


class ConversationPublic(SQLModel):
    """Public representation of a conversation."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    title: Optional[str]
    archived: bool
