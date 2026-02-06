"""
Business logic layer for the Todo application.

Provides methods for managing todo items following single responsibility principle.
"""


from typing import List, Optional
from .models import TodoItem
from .repository import TodoRepository


class TodoService:
    """
    Service layer for todo operations.
    Contains business logic for add, view, update, delete, and mark complete operations.
    """

    def __init__(self, repository: TodoRepository = None):
        """
        Initialize the service with a repository.

        Args:
            repository (TodoRepository): Repository to use for data operations.
                                       If None, a new repository will be created.
        """
        self.repository = repository if repository is not None else TodoRepository()

    def add_todo(self, title: str, description: str = "") -> TodoItem:
        """
        Add a new todo item with validation.

        Args:
            title (str): Title of the new todo item
            description (str): Description of the new todo item (optional)

        Returns:
            TodoItem: The newly created TodoItem instance

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        # Validate the title before creating the item
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty or whitespace only")

        return self.repository.create(title, description)

    def get_all_todos(self) -> List[TodoItem]:
        """
        Get all todo items.

        Returns:
            List[TodoItem]: List of all todo items
        """
        return self.repository.get_all()

    def update_todo(self, item_id: int, title: str = None, description: str = None) -> Optional[TodoItem]:
        """
        Update an existing todo item.

        Args:
            item_id (int): ID of the todo item to update
            title (str): New title (optional)
            description (str): New description (optional)

        Returns:
            TodoItem: The updated todo item if found, None otherwise

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        # Validate the title if it's being updated
        if title is not None and (not title or not title.strip()):
            raise ValueError("Title is required and cannot be empty or whitespace only")

        return self.repository.update(item_id, title, description)

    def delete_todo(self, item_id: int) -> bool:
        """
        Delete a todo item by ID.

        Args:
            item_id (int): ID of the todo item to delete

        Returns:
            bool: True if the item was deleted, False if it didn't exist
        """
        return self.repository.delete(item_id)

    def toggle_completion(self, item_id: int) -> Optional[TodoItem]:
        """
        Toggle the completion status of a todo item.

        Args:
            item_id (int): ID of the todo item to toggle

        Returns:
            TodoItem: The updated todo item if found, None otherwise
        """
        return self.repository.toggle_completion(item_id)

    def get_todo_by_id(self, item_id: int) -> Optional[TodoItem]:
        """
        Get a todo item by ID.

        Args:
            item_id (int): ID of the todo item to retrieve

        Returns:
            TodoItem: The todo item if found, None otherwise
        """
        return self.repository.get_by_id(item_id)