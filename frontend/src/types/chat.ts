/**
 * Chat-related TypeScript types and interfaces
 */

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  metadata?: {
    tool_calls?: Array<{
      tool_name: string;
      tool_call_id: string;
      arguments: Record<string, any>;
      result: any;
    }>;
  };
}

export interface ChatError {
  message: string;
  status?: number;
}
