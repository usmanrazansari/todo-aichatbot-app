"""
Chat API routes for AI-powered task management.

This module provides the chat endpoint that enables natural language
interaction with the task management system.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.db.database import get_session
from src.utils.jwt_handler import verify_token
from src.services import conversation_service, message_service
from src.ai.agent import get_agent
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


# Request/Response models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    conversation_id: str
    metadata: Optional[Dict[str, Any]] = None


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user ID from the JWT token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        User ID as string

    Raises:
        HTTPException: If token is invalid
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


@router.post("/chat", response_model=ChatResponse)
def chat(
    chat_request: ChatRequest,
    user_id: str = Path(..., description="The ID of the user"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint for natural language task management.

    This endpoint:
    1. Authenticates the user via JWT
    2. Retrieves or creates a conversation
    3. Loads conversation history
    4. Invokes the AI agent with the user's message
    5. Persists the user message and assistant response
    6. Returns the assistant's response and conversation ID

    Args:
        chat_request: Chat request containing user message and optional conversation_id
        user_id: User ID from path (must match authenticated user)
        current_user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        ChatResponse with assistant's response and conversation_id

    Raises:
        HTTPException: If authentication fails or user_id mismatch
    """
    try:
        # Verify user_id in path matches authenticated user
        if user_id != current_user_id:
            logger.warning(f"User ID mismatch: path={user_id}, token={current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: user ID in path does not match authenticated user"
            )

        logger.info(f"Chat request from user {user_id}: {chat_request.message[:50]}...")

        # Get or create conversation
        conversation = None
        if chat_request.conversation_id:
            # Resume existing conversation
            conversation = conversation_service.get_conversation(
                session,
                chat_request.conversation_id,
                user_id
            )
            if not conversation:
                logger.warning(f"Conversation {chat_request.conversation_id} not found, creating new")

        if not conversation:
            # Create new conversation
            conversation = conversation_service.create_conversation(
                session,
                user_id,
                title=None  # Could auto-generate from first message
            )
            logger.info(f"Created new conversation {conversation.id}")

        # Load conversation history
        history_messages = message_service.get_conversation_history(
            session,
            conversation.id,
            user_id,
            limit=50,
            days_limit=30
        )

        # Format history for OpenAI
        conversation_history = message_service.format_messages_for_openai(history_messages)

        # Get AI agent
        agent = get_agent()

        # Process message with AI agent
        agent_result = agent.process_message(
            user_message=chat_request.message,
            conversation_history=conversation_history,
            user_id=user_id,
            session=session
        )

        assistant_response = agent_result["response"]
        tool_calls = agent_result.get("tool_calls", [])

        # Persist user message
        message_service.add_message(
            session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=chat_request.message
        )

        # Persist assistant response
        message_service.add_message(
            session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=assistant_response
        )

        # Persist tool calls as messages (for debugging/analytics)
        for tool_call in tool_calls:
            message_service.add_message(
                session,
                conversation_id=conversation.id,
                user_id=user_id,
                role="tool",
                content=str(tool_call.get("result", {})),
                tool_call_id=tool_call.get("tool_call_id"),
                tool_name=tool_call.get("tool_name")
            )

        logger.info(f"Chat response generated for conversation {conversation.id}")

        # Return response
        return ChatResponse(
            response=assistant_response,
            conversation_id=conversation.id,
            metadata={
                "tool_calls": tool_calls
            } if tool_calls else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/conversations")
def list_conversations(
    user_id: str = Path(..., description="The ID of the user"),
    current_user_id: str = Depends(get_current_user_id),
    include_archived: bool = False,
    session: Session = Depends(get_session)
):
    """
    List all conversations for the authenticated user.

    Args:
        user_id: User ID from path (must match authenticated user)
        current_user_id: Authenticated user ID from JWT token
        include_archived: Whether to include archived conversations
        session: Database session

    Returns:
        List of conversations

    Raises:
        HTTPException: If authentication fails or user_id mismatch
    """
    try:
        # Verify user_id in path matches authenticated user
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: user ID in path does not match authenticated user"
            )

        conversations = conversation_service.list_user_conversations(
            session,
            user_id,
            include_archived=include_archived
        )

        return {
            "conversations": [
                {
                    "id": conv.id,
                    "user_id": conv.user_id,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "archived": conv.archived
                }
                for conv in conversations
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"List conversations error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
