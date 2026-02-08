from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Message(SQLModel, table=True):
    """
    Message model representing a single message in a conversation.

    Messages can be from user, assistant, system, or tool roles.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique message identifier (UUID)"
    )

    conversation_id: str = Field(
        foreign_key="conversation.id",
        index=True,
        description="Parent conversation ID"
    )

    user_id: str = Field(
        index=True,
        description="Owner of the conversation (denormalized for security)"
    )

    role: str = Field(
        max_length=20,
        description="Message role: 'user', 'assistant', 'system', or 'tool'"
    )

    content: str = Field(
        description="Message text content or tool result (JSON string for tool messages)"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the message was created"
    )

    tool_call_id: Optional[str] = Field(
        default=None,
        description="OpenAI tool call ID (for tool messages)"
    )

    tool_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Name of the tool that was called (for tool messages)"
    )


class MessageCreate(SQLModel):
    """Model for creating new messages."""
    conversation_id: str
    role: str = Field(max_length=20)
    content: str
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None


class MessagePublic(SQLModel):
    """Public representation of a message."""
    id: str
    conversation_id: str
    user_id: str
    role: str
    content: str
    created_at: datetime
    tool_call_id: Optional[str]
    tool_name: Optional[str]
