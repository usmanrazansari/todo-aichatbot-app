/**
 * Chat API service
 *
 * Handles communication with the backend chat endpoint.
 */

import { ChatRequest, ChatResponse } from '../types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Send a message to the chat endpoint
 *
 * @param message - User message
 * @param conversationId - Optional conversation ID to resume
 * @param token - JWT authentication token
 * @param userId - User ID for API path
 * @returns Chat response with assistant message and conversation ID
 */
export async function sendMessage(
  message: string,
  conversationId: string | null,
  token: string,
  userId: string
): Promise<ChatResponse> {
  const requestBody: ChatRequest = {
    message,
  };

  if (conversationId) {
    requestBody.conversation_id = conversationId;
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Unauthorized - please log in again');
    }
    if (response.status === 403) {
      throw new Error('Access forbidden');
    }
    if (response.status === 500) {
      throw new Error('Server error - please try again later');
    }
    throw new Error(`Request failed with status ${response.status}`);
  }

  const data: ChatResponse = await response.json();
  return data;
}

/**
 * Get list of conversations for the user
 *
 * @param token - JWT authentication token
 * @param userId - User ID for API path
 * @returns List of conversations
 */
export async function getConversations(
  token: string,
  userId: string
): Promise<any[]> {
  const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch conversations: ${response.status}`);
  }

  const data = await response.json();
  return data.conversations || [];
}
