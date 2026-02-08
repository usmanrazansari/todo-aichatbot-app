import React from 'react';
import { useRouter } from 'next/router';
import ChatInterface from '../components/ChatInterface';

/**
 * Chat page component
 *
 * Provides the main chat interface for AI-powered task management.
 */
export default function ChatPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Task Assistant</h1>
          <p className="text-gray-600 mt-2">
            Chat with your AI assistant to manage your tasks
          </p>
        </div>

        <ChatInterface />

        <div className="mt-4 text-center">
          <button
            onClick={() => router.push('/dashboard')}
            className="text-blue-600 hover:text-blue-800 text-sm"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
