# Data Model: AI-Powered Chatbot via MCP

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-02-08
**Status**: Phase 1 Design

## Overview

This document defines the database schema for conversation persistence in the AI-powered chatbot feature. The design extends the existing Phase II database with two new tables while maintaining compatibility with the existing Task model.

## Design Principles

1. **Stateless Backend**: All conversation state persisted to database
2. **User Ownership**: All entities scoped to user_id for security
3. **Audit Trail**: Timestamps on all entities for debugging and analytics
4. **Denormalization**: user_id duplicated in Message for fast security checks
5. **Compatibility**: Follows existing Phase II SQLModel patterns

## Entity Relationship Diagram

```
┌─────────────────┐
│   Conversation  │
│─────────────────│
│ id (PK)         │
│ user_id (FK)    │◄──────┐
│ created_at      │       │
│ updated_at      │       │
│ title           │       │
│ archived        │       │
└─────────────────┘       │
         │                │
         │ 1:N            │
         ▼                │
┌─────────────────┐       │
│    Message      │       │
│─────────────────│       │
│ id (PK)         │       │
│ conversation_id │───────┘
│ user_id (FK)    │ (denormalized)
│ role            │
│ content         │
│ created_at      │
│ tool_call_id    │
│ tool_name       │
└─────────────────┘

Note: user_id is not a foreign key to User table
      (Better Auth manages users separately)
```

## Table Definitions

### Conversation Table

**Purpose**: Represents a chat conversation between a user and the AI assistant.

**SQLModel Definition**:

```python
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
```

**Field Descriptions**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | string (UUID) | Primary Key, Not Null | Unique identifier for the conversation |
| `user_id` | string | Not Null, Indexed | Owner of the conversation (from JWT token) |
| `created_at` | datetime | Not Null, Default: now() | Timestamp when conversation was created |
| `updated_at` | datetime | Not Null, Default: now() | Timestamp when conversation was last updated |
| `title` | string | Nullable, Max 255 chars | Optional human-readable title |
| `archived` | boolean | Not Null, Default: false | Soft delete flag |

**Indexes**:
- Primary key on `id` (auto-created)
- Index on `user_id` for fast user conversation queries
- Composite index on `(user_id, updated_at DESC)` for listing user's conversations

**Business Rules**:
1. Conversations are owned by a single user (no sharing in Phase III)
2. `updated_at` should be updated whenever a new message is added
3. Archived conversations are hidden from default queries but not deleted
4. Title can be auto-generated from first user message or set manually

---

### Message Table

**Purpose**: Represents a single message in a conversation (user, assistant, system, or tool).

**SQLModel Definition**:

```python
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
```

**Field Descriptions**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | string (UUID) | Primary Key, Not Null | Unique identifier for the message |
| `conversation_id` | string (UUID) | Foreign Key, Not Null, Indexed | Parent conversation |
| `user_id` | string | Not Null, Indexed | Owner (denormalized from conversation) |
| `role` | string | Not Null, Max 20 chars | Message role (user/assistant/system/tool) |
| `content` | string | Not Null | Message text or tool result |
| `created_at` | datetime | Not Null, Default: now() | Timestamp when message was created |
| `tool_call_id` | string | Nullable | OpenAI tool call ID (for tool messages) |
| `tool_name` | string | Nullable, Max 100 chars | Tool name (for debugging/analytics) |

**Indexes**:
- Primary key on `id` (auto-created)
- Foreign key index on `conversation_id` (auto-created)
- Index on `user_id` for security checks
- Composite index on `(conversation_id, created_at DESC)` for conversation retrieval

**Business Rules**:
1. Messages are immutable once created (no updates, only creates)
2. Messages are ordered by `created_at` within a conversation
3. `role` must be one of: "user", "assistant", "system", "tool"
4. `tool_call_id` and `tool_name` are only set for tool messages
5. `user_id` is denormalized from conversation for fast security checks
6. Tool messages store JSON-serialized results in `content`

**Role Definitions**:
- **user**: Message from the end user
- **assistant**: Message from the AI assistant
- **system**: System prompt or instructions (typically first message)
- **tool**: Result from a tool invocation

---

## Existing Task Model (Phase II)

**Reference**: The Task model from Phase II is reused by MCP tools.

```python
class Task(SQLModel, table=True):
    """Task model representing a todo item owned by a specific user."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**No changes required** to the Task model. MCP tools will interact with tasks through the existing service layer.

---

## Database Indexes

### Required Indexes

```sql
-- Conversation indexes
CREATE INDEX idx_conversation_user ON conversation(user_id);
CREATE INDEX idx_conversation_user_updated ON conversation(user_id, updated_at DESC);

-- Message indexes
CREATE INDEX idx_message_conversation ON message(conversation_id);
CREATE INDEX idx_message_user ON message(user_id);
CREATE INDEX idx_message_conversation_created ON message(conversation_id, created_at DESC);
```

### Index Rationale

| Index | Purpose | Query Pattern |
|-------|---------|---------------|
| `idx_conversation_user` | List user's conversations | `WHERE user_id = ?` |
| `idx_conversation_user_updated` | List user's recent conversations | `WHERE user_id = ? ORDER BY updated_at DESC` |
| `idx_message_conversation` | Get messages for conversation | `WHERE conversation_id = ?` |
| `idx_message_user` | Security check (user owns message) | `WHERE user_id = ?` |
| `idx_message_conversation_created` | Get conversation history | `WHERE conversation_id = ? ORDER BY created_at DESC LIMIT 50` |

---

## Data Access Patterns

### Pattern 1: Create New Conversation

```python
def create_conversation(session: Session, user_id: str, title: str = None) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation(user_id=user_id, title=title)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

### Pattern 2: Add Message to Conversation

```python
def add_message(
    session: Session,
    conversation_id: str,
    user_id: str,
    role: str,
    content: str,
    tool_call_id: str = None,
    tool_name: str = None
) -> Message:
    """Add a message to a conversation."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_call_id=tool_call_id,
        tool_name=tool_name
    )
    session.add(message)

    # Update conversation updated_at
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(message)
    return message
```

### Pattern 3: Get Conversation History

```python
def get_conversation_history(
    session: Session,
    conversation_id: str,
    user_id: str,
    limit: int = 50
) -> List[Message]:
    """Get recent messages for a conversation."""
    # Verify user owns conversation
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise ValueError("Conversation not found or access denied")

    # Get recent messages
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    ).all()

    # Reverse to chronological order
    return list(reversed(messages))
```

### Pattern 4: List User's Conversations

```python
def list_user_conversations(
    session: Session,
    user_id: str,
    include_archived: bool = False
) -> List[Conversation]:
    """List all conversations for a user."""
    query = select(Conversation).where(Conversation.user_id == user_id)

    if not include_archived:
        query = query.where(Conversation.archived == False)

    query = query.order_by(Conversation.updated_at.desc())

    return session.exec(query).all()
```

---

## Migration Strategy

### Development (SQLite)

SQLModel automatically creates tables on startup:

```python
# In backend/src/main.py
from src.models.conversation import Conversation
from src.models.message import Message

@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")
```

### Production (PostgreSQL/MySQL)

Use Alembic for migrations:

```bash
# Generate migration
alembic revision --autogenerate -m "Add conversation and message tables"

# Review generated migration in alembic/versions/

# Apply migration
alembic upgrade head
```

---

## Data Retention & Cleanup

### Retention Policy

- **Active conversations**: No automatic deletion
- **Archived conversations**: Retained indefinitely (user-initiated archive)
- **Message history**: Limited to 50 messages per conversation in AI context (but all stored)

### Cleanup Strategies (Future)

1. **Hard delete archived conversations** older than 90 days
2. **Summarize old messages** and replace with summary
3. **Export and archive** conversations to cold storage

**Phase III**: No automatic cleanup. Manual deletion only.

---

## Security Considerations

1. **User Ownership**: All queries must filter by `user_id` from JWT token
2. **Denormalized user_id**: Message table includes `user_id` for fast security checks
3. **No Cross-User Access**: Conversations and messages are strictly scoped to owner
4. **Input Validation**: Message content should be sanitized (no XSS in stored data)
5. **Audit Trail**: All entities have timestamps for debugging and compliance

---

## Performance Considerations

1. **Indexes**: Composite indexes on common query patterns
2. **Limit Message History**: Retrieve only 50 most recent messages
3. **Denormalization**: `user_id` in Message avoids JOIN for security checks
4. **Connection Pooling**: Use SQLModel's built-in connection pooling
5. **Query Optimization**: Use `select()` with filters instead of loading all records

**Expected Performance**:
- Conversation creation: <10ms
- Message insertion: <10ms
- History retrieval (50 messages): <100ms
- User conversation list: <50ms

---

## Testing Strategy

### Unit Tests

```python
def test_create_conversation():
    """Test conversation creation."""
    conversation = create_conversation(session, user_id="user123", title="Test")
    assert conversation.id is not None
    assert conversation.user_id == "user123"
    assert conversation.title == "Test"

def test_add_message():
    """Test adding message to conversation."""
    conversation = create_conversation(session, user_id="user123")
    message = add_message(
        session,
        conversation_id=conversation.id,
        user_id="user123",
        role="user",
        content="Hello"
    )
    assert message.id is not None
    assert message.role == "user"
    assert message.content == "Hello"

def test_get_conversation_history():
    """Test retrieving conversation history."""
    conversation = create_conversation(session, user_id="user123")
    add_message(session, conversation.id, "user123", "user", "Message 1")
    add_message(session, conversation.id, "user123", "assistant", "Message 2")

    history = get_conversation_history(session, conversation.id, "user123")
    assert len(history) == 2
    assert history[0].content == "Message 1"
    assert history[1].content == "Message 2"
```

### Integration Tests

- Test conversation creation via API
- Test message persistence across requests
- Test conversation history retrieval
- Test user ownership enforcement
- Test conversation list pagination

---

## Summary

This data model provides:
- ✅ Stateless backend support (all state in database)
- ✅ User ownership and security
- ✅ Efficient conversation history retrieval
- ✅ Audit trail with timestamps
- ✅ Compatibility with existing Phase II patterns
- ✅ Scalable design with proper indexing

**Next Steps**: Create API contracts and quickstart guide.
