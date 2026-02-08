"""
MCP Server for Todo Task Management

This module implements an MCP (Model Context Protocol) server that exposes
task management operations as tools for AI agents.

Since the official MCP SDK may not be available, this implements a simplified
MCP-style interface that bridges to OpenAI function calling.
"""

from typing import Dict, List, Any, Callable
import logging

logger = logging.getLogger(__name__)


class MCPServer:
    """
    Simplified MCP server for task management tools.

    This server maintains a registry of tools and their schemas,
    and provides methods to invoke tools and convert schemas to
    OpenAI function calling format.
    """

    def __init__(self, name: str = "todo-tools"):
        """
        Initialize MCP server.

        Args:
            name: Server name/namespace
        """
        self.name = name
        self.tools: Dict[str, Dict[str, Any]] = {}
        logger.info(f"Initialized MCP server: {name}")

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable
    ) -> None:
        """
        Register a tool with the MCP server.

        Args:
            name: Tool name
            description: Tool description
            parameters: JSON Schema for tool parameters
            handler: Function to execute when tool is called
        """
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "handler": handler
        }
        logger.info(f"Registered tool: {name}")

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Get all tool schemas in OpenAI function calling format.

        Returns:
            List of tool schemas compatible with OpenAI API
        """
        schemas = []
        for tool_name, tool_data in self.tools.items():
            schema = {
                "type": "function",
                "function": {
                    "name": tool_data["name"],
                    "description": tool_data["description"],
                    "parameters": tool_data["parameters"]
                }
            }
            schemas.append(schema)

        logger.debug(f"Generated {len(schemas)} tool schemas")
        return schemas

    def invoke_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoke a tool by name with given arguments.

        Args:
            tool_name: Name of the tool to invoke
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
        """
        if tool_name not in self.tools:
            error_msg = f"Tool not found: {tool_name}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }

        tool = self.tools[tool_name]
        handler = tool["handler"]

        try:
            logger.info(f"Invoking tool: {tool_name}")
            result = handler(**arguments)
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        except Exception as e:
            error_msg = f"Tool execution error: {str(e)}"
            logger.error(f"Tool {tool_name} failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())


# Global MCP server instance
mcp_server = MCPServer(name="todo-tools")


# Import and register all tools
from src.mcp.tools.add_task import add_task_tool, ADD_TASK_SCHEMA
from src.mcp.tools.list_tasks import list_tasks_tool, LIST_TASKS_SCHEMA
from src.mcp.tools.update_task import update_task_tool, UPDATE_TASK_SCHEMA
from src.mcp.tools.complete_task import complete_task_tool, COMPLETE_TASK_SCHEMA
from src.mcp.tools.delete_task import delete_task_tool, DELETE_TASK_SCHEMA


def register_all_tools():
    """Register all MCP tools with the server."""

    # Register add_task tool
    mcp_server.register_tool(
        name="add_task",
        description="Add a new task to the user's todo list. Use this when the user wants to create a new task, add something to their list, or remember to do something.",
        parameters=ADD_TASK_SCHEMA,
        handler=add_task_tool
    )

    # Register list_tasks tool
    mcp_server.register_tool(
        name="list_tasks",
        description="Retrieve all tasks for the user. Use this when the user wants to see their tasks, check what's on their list, or review their todos.",
        parameters=LIST_TASKS_SCHEMA,
        handler=list_tasks_tool
    )

    # Register update_task tool
    mcp_server.register_tool(
        name="update_task",
        description="Update an existing task's title, description, or completion status. Use this when the user wants to modify a task, change its details, or mark it as complete/incomplete.",
        parameters=UPDATE_TASK_SCHEMA,
        handler=update_task_tool
    )

    # Register complete_task tool
    mcp_server.register_tool(
        name="complete_task",
        description="Mark a task as completed. Use this when the user indicates they have finished a task, completed something, or are done with a todo item.",
        parameters=COMPLETE_TASK_SCHEMA,
        handler=complete_task_tool
    )

    # Register delete_task tool
    mcp_server.register_tool(
        name="delete_task",
        description="Permanently delete a task from the user's list. Use this when the user wants to remove a task, delete something from their list, or get rid of a todo item.",
        parameters=DELETE_TASK_SCHEMA,
        handler=delete_task_tool
    )

    logger.info(f"Registered {len(mcp_server.list_tools())} MCP tools")


# Auto-register tools on module import
register_all_tools()

