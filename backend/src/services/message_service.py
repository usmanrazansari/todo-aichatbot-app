from sqlmodel import Session, select
from src.models.message import Message, MessageCreate
from src.services.conversation_service import update_conversation_timestamp
from typing import List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def add_message(
    session: Session,
    conversation_id: str,
    user_id: str,
    role: str,
    content: str,
    tool_call_id: Optional[str] = None,
    tool_name: Optional[str] = None
) -> Message:
    """
    Add a message to a conversation.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user (owner of conversation)
        role: Message role ('user', 'assistant', 'system', 'tool')
        content: Message content
        tool_call_id: Optional OpenAI tool call ID (for tool messages)
        tool_name: Optional tool name (for tool messages)

    Returns:
        Created Message object
    """
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_call_id=tool_call_id,
        tool_name=tool_name
    )

    session.add(message)

    # Update conversation timestamp
    update_conversation_timestamp(session, conversation_id)

    session.commit()
    session.refresh(message)

    logger.info(f"Added {role} message to conversation {conversation_id}")
    return message


def get_conversation_history(
    session: Session,
    conversation_id: str,
    user_id: str,
    limit: int = 50,
    days_limit: int = 30
) -> List[Message]:
    """
    Get conversation history (recent messages).

    Retrieves up to `limit` most recent messages or messages from the last
    `days_limit` days, whichever is smaller.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user (for ownership verification)
        limit: Maximum number of messages to retrieve (default: 50)
        days_limit: Maximum age of messages in days (default: 30)

    Returns:
        List of Message objects ordered chronologically (oldest first)
    """
    # Calculate cutoff date
    cutoff_date = datetime.utcnow() - timedelta(days=days_limit)

    # Query messages
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id,
        Message.created_at >= cutoff_date
    ).order_by(Message.created_at.desc()).limit(limit)

    messages = session.exec(statement).all()

    # Reverse to chronological order (oldest first)
    messages_list = list(reversed(messages))

    logger.info(
        f"Retrieved {len(messages_list)} messages from conversation {conversation_id} "
        f"for user {user_id}"
    )

    return messages_list


def get_messages_by_conversation(
    session: Session,
    conversation_id: str,
    user_id: str
) -> List[Message]:
    """
    Get all messages for a conversation (no limit).

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user (for ownership verification)

    Returns:
        List of Message objects ordered chronologically
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.created_at.asc())

    messages = session.exec(statement).all()

    logger.info(
        f"Retrieved all {len(messages)} messages from conversation {conversation_id}"
    )

    return list(messages)


def format_messages_for_openai(messages: List[Message]) -> List[dict]:
    """
    Format messages for OpenAI API.

    Converts Message objects to OpenAI chat completion format.
    Filters out tool-related messages to avoid API compatibility issues.

    Args:
        messages: List of Message objects

    Returns:
        List of message dictionaries in OpenAI format
    """
    formatted_messages = []

    for msg in messages:
        # Skip tool messages - they're not needed in conversation history
        # and can cause API compatibility issues
        if msg.role == "tool":
            continue

        # Skip assistant messages that were tool calls (content is None)
        if msg.role == "assistant" and msg.content is None:
            continue

        message_dict = {
            "role": msg.role,
            "content": msg.content
        }

        formatted_messages.append(message_dict)

    return formatted_messages
