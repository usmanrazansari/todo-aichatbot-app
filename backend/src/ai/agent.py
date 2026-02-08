"""
AI Agent using OpenRouter API with function calling.

This module implements the AI agent that orchestrates task management
through natural language conversation and MCP tool invocation.
"""

import requests
from src.ai.prompts import get_system_prompt
from src.mcp.server import mcp_server
from sqlmodel import Session
from typing import List, Dict, Any, Optional
import json
import os
import logging

logger = logging.getLogger(__name__)


class TaskManagementAgent:
    """
    AI agent for task management using OpenRouter API with function calling.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the AI agent.

        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            model: AI model to use (defaults to AI_MODEL env var or openai/gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("AI_MODEL", "openai/gpt-4o-mini")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

        if not self.api_key:
            raise ValueError("OpenRouter API key not provided and OPENROUTER_API_KEY env var not set")

        self.system_prompt = get_system_prompt()

        logger.info(f"Initialized TaskManagementAgent with OpenRouter model: {self.model}")

    def _call_openrouter_api(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Call OpenRouter API with messages and optional tools.

        Args:
            messages: List of message dictionaries
            tools: Optional list of tool schemas

        Returns:
            API response dictionary
        """
        payload = {
            "model": self.model,
            "messages": messages
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response.

        This method:
        1. Adds the user message to conversation history
        2. Calls Bytez API with function calling enabled
        3. Handles tool calls by invoking MCP tools
        4. Returns the assistant's response and metadata

        Args:
            user_message: The user's message
            conversation_history: Previous messages in the conversation
            user_id: ID of the user (for tool invocation)
            session: Database session (for tool invocation)

        Returns:
            Dictionary containing:
                - response: Assistant's text response
                - tool_calls: List of tool calls made (for logging)
        """
        try:
            # Build messages for Bytez API
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]

            # Add conversation history
            messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Get MCP tool schemas
            tools = mcp_server.get_tool_schemas()

            logger.info(f"Calling OpenRouter API with {len(messages)} messages and {len(tools)} tools")

            # Call OpenRouter API with function calling
            response = self._call_openrouter_api(messages, tools)

            # Extract assistant message
            if "choices" in response and len(response["choices"]) > 0:
                assistant_message = response["choices"][0]["message"]
            else:
                raise ValueError("Invalid response from Bytez API")

            tool_calls_metadata = []

            # Check if the assistant wants to call tools
            if assistant_message.get("tool_calls"):
                logger.info(f"Assistant requested {len(assistant_message['tool_calls'])} tool calls")

                # Process each tool call
                for tool_call in assistant_message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])

                    logger.info(f"Invoking tool: {tool_name} with args: {tool_args}")

                    # Inject user_id and session into tool arguments
                    tool_args["user_id"] = user_id
                    tool_args["session"] = session

                    # Invoke MCP tool
                    tool_result = mcp_server.invoke_tool(tool_name, tool_args)

                    # Store metadata
                    tool_calls_metadata.append({
                        "tool_name": tool_name,
                        "tool_call_id": tool_call["id"],
                        "arguments": {k: v for k, v in tool_args.items() if k not in ["session"]},
                        "result": tool_result
                    })

                    # Add tool call and result to messages for next API call
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call["id"],
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": tool_call["function"]["arguments"]
                            }
                        }]
                    })

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(tool_result)
                    })

                # Call OpenRouter API again with tool results to get final response
                logger.info("Calling OpenRouter API again with tool results")
                final_response = self._call_openrouter_api(messages)

                if "choices" in final_response and len(final_response["choices"]) > 0:
                    final_message = final_response["choices"][0]["message"]["content"]
                else:
                    final_message = "Task completed successfully."

            else:
                # No tool calls, use the assistant's direct response
                final_message = assistant_message.get("content", "I'm here to help with your tasks!")

            logger.info("Agent processing complete")

            return {
                "response": final_message,
                "tool_calls": tool_calls_metadata
            }

        except requests.exceptions.RequestException as e:
            error_msg = f"OpenRouter API error: {str(e)}"
            logger.error(error_msg)
            return {
                "response": "I'm sorry, I encountered an error connecting to the AI service. Please try again.",
                "tool_calls": [],
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Agent error: {str(e)}"
            logger.error(error_msg)
            return {
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "error": error_msg
            }


# Global agent instance (initialized on first use)
_agent_instance: Optional[TaskManagementAgent] = None


def get_agent() -> TaskManagementAgent:
    """
    Get or create the global agent instance.

    Returns:
        TaskManagementAgent instance
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TaskManagementAgent()
    return _agent_instance
