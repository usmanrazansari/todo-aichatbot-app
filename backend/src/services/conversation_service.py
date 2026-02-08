from sqlmodel import Session, select
from src.models.conversation import Conversation, ConversationCreate, ConversationUpdate
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def create_conversation(
    session: Session,
    user_id: str,
    title: Optional[str] = None
) -> Conversation:
    """
    Create a new conversation for a user.

    Args:
        session: Database session
        user_id: ID of the user creating the conversation
        title: Optional conversation title

    Returns:
        Created Conversation object
    """
    conversation = Conversation(user_id=user_id, title=title)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    logger.info(f"Created conversation {conversation.id} for user {user_id}")
    return conversation


def get_conversation(
    session: Session,
    conversation_id: str,
    user_id: str
) -> Optional[Conversation]:
    """
    Get a conversation by ID, ensuring user ownership.

    Args:
        session: Database session
        conversation_id: ID of the conversation to retrieve
        user_id: ID of the user (for ownership verification)

    Returns:
        Conversation object if found and owned by user, None otherwise
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = session.exec(statement).first()

    if conversation:
        logger.info(f"Retrieved conversation {conversation_id} for user {user_id}")
    else:
        logger.warning(f"Conversation {conversation_id} not found or access denied for user {user_id}")

    return conversation


def list_user_conversations(
    session: Session,
    user_id: str,
    include_archived: bool = False
) -> List[Conversation]:
    """
    List all conversations for a user.

    Args:
        session: Database session
        user_id: ID of the user
        include_archived: Whether to include archived conversations

    Returns:
        List of Conversation objects ordered by updated_at descending
    """
    statement = select(Conversation).where(Conversation.user_id == user_id)

    if not include_archived:
        statement = statement.where(Conversation.archived == False)

    statement = statement.order_by(Conversation.updated_at.desc())

    conversations = session.exec(statement).all()
    logger.info(f"Retrieved {len(conversations)} conversations for user {user_id}")

    return list(conversations)


def update_conversation(
    session: Session,
    conversation_id: str,
    user_id: str,
    update_data: ConversationUpdate
) -> Optional[Conversation]:
    """
    Update a conversation.

    Args:
        session: Database session
        conversation_id: ID of the conversation to update
        user_id: ID of the user (for ownership verification)
        update_data: Update data

    Returns:
        Updated Conversation object if found and owned by user, None otherwise
    """
    conversation = get_conversation(session, conversation_id, user_id)

    if not conversation:
        return None

    # Update fields
    if update_data.title is not None:
        conversation.title = update_data.title
    if update_data.archived is not None:
        conversation.archived = update_data.archived

    conversation.updated_at = datetime.utcnow()

    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    logger.info(f"Updated conversation {conversation_id} for user {user_id}")
    return conversation


def update_conversation_timestamp(
    session: Session,
    conversation_id: str
) -> None:
    """
    Update the updated_at timestamp of a conversation.

    This is called when a new message is added to the conversation.

    Args:
        session: Database session
        conversation_id: ID of the conversation to update
    """
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        logger.debug(f"Updated timestamp for conversation {conversation_id}")
