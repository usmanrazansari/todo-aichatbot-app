"""
Formatting utilities for the Todo application.

Contains functions for formatting todo items for display.
"""


from typing import List
from .models import TodoItem


def format_todo_item(todo: TodoItem) -> str:
    """
    Format a single todo item for display.

    Args:
        todo (TodoItem): The todo item to format

    Returns:
        str: Formatted string representation of the todo item
    """
    status_symbol = "X" if todo.completion_status else "O"
    status_text = "Completed" if todo.completion_status else "Pending"

    formatted = f"[{status_symbol}] {todo.id}. {todo.title} ({status_text})"

    if todo.description:
        formatted += f"\n      Description: {todo.description}"

    return formatted


def format_todo_list(todos: List[TodoItem]) -> str:
    """
    Format a list of todo items for display.

    Args:
        todos (List[TodoItem]): List of todo items to format

    Returns:
        str: Formatted string representation of the todo list
    """
    if not todos:
        return "No todos found."

    formatted_items = []
    for todo in todos:
        formatted_items.append(format_todo_item(todo))

    return "\n".join(formatted_items)


def format_todo_summary(todo: TodoItem) -> str:
    """
    Format a brief summary of a todo item.

    Args:
        todo (TodoItem): The todo item to format

    Returns:
        str: Brief formatted summary of the todo item
    """
    status = "X" if todo.completion_status else "O"
    return f"[{status}] {todo.id}. {todo.title}"