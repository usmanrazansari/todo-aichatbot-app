/**
 * ChatInterface component
 *
 * Provides a chat UI for interacting with the AI task management assistant.
 */

import React, { useState, useEffect } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { sendMessage } from '../services/chatApi';
import { ChatMessage } from '../types/chat';
import { getAuthToken, getUserIdFromToken, isAuthenticated } from '../services/auth';

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    // Check authentication first
    if (!isAuthenticated()) {
      window.location.href = '/login';
      return;
    }

    const savedConversationId = localStorage.getItem('chat_conversation_id');
    if (savedConversationId) {
      setConversationId(savedConversationId);
    }

    // Get token and userId from auth service
    const authToken = getAuthToken();
    const authUserId = getUserIdFromToken();

    setToken(authToken);
    setUserId(authUserId);

    // Add welcome message
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          role: 'assistant',
          content: 'Hi! I\'m your task management assistant. I can help you add, view, update, complete, and delete tasks. What would you like to do?',
          timestamp: new Date(),
        },
      ]);
    }
  }, []);

  // Save conversation ID to localStorage when it changes
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem('chat_conversation_id', conversationId);
    }
  }, [conversationId]);

  const handleSend = async (message: string) => {
    if (!message.trim()) return;

    // Check authentication
    if (!token || !userId) {
      setError('Please log in to use the chat');
      return;
    }

    // Add user message to UI
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setError(null);
    setIsTyping(true);

    try {
      // Send message to backend
      const response = await sendMessage(message, conversationId, token, userId);

      // Update conversation ID if new
      if (response.conversation_id && response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to UI
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Add error message to chat
      const errorChatMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorChatMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleNewConversation = () => {
    setConversationId(null);
    localStorage.removeItem('chat_conversation_id');
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Hi! I\'m your task management assistant. I can help you add, view, update, complete, and delete tasks. What would you like to do?',
        timestamp: new Date(),
      },
    ]);
    setError(null);
  };

  return (
    <div className="chat-interface">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="mb-4 flex justify-between items-center">
        <div className="text-sm text-gray-600">
          {conversationId ? (
            <span>Conversation ID: {conversationId.substring(0, 8)}...</span>
          ) : (
            <span>New conversation</span>
          )}
        </div>
        <button
          onClick={handleNewConversation}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          New Conversation
        </button>
      </div>

      <div style={{ position: 'relative', height: '500px' }}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator={
                isTyping ? <TypingIndicator content="Assistant is typing" /> : null
              }
            >
              {messages.map((msg) => (
                <Message
                  key={msg.id}
                  model={{
                    message: msg.content,
                    sentTime: msg.timestamp.toISOString(),
                    sender: msg.role === 'user' ? 'You' : 'Assistant',
                    direction: msg.role === 'user' ? 'outgoing' : 'incoming',
                    position: 'single',
                  }}
                />
              ))}
            </MessageList>
            <MessageInput
              placeholder="Type your message here..."
              onSend={handleSend}
              attachButton={false}
            />
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
}
