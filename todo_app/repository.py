"""
Repository layer for the Todo application.

Handles in-memory storage and retrieval of todo items.
"""


from typing import Dict, List, Optional
from .models import TodoItem


class TodoRepository:
    """
    In-memory repository for storing and managing TodoItem objects.
    Implements CRUD operations for todo items.
    """

    def __init__(self):
        """Initialize the repository with an empty storage."""
        self._storage: Dict[int, TodoItem] = {}
        self._next_id = 1

    def create(self, title: str, description: str = "") -> TodoItem:
        """
        Create a new todo item with a unique ID and pending status.

        Args:
            title (str): Title of the new todo item
            description (str): Description of the new todo item (optional)

        Returns:
            TodoItem: The newly created TodoItem instance
        """
        new_item = TodoItem(
            item_id=self._next_id,
            title=title,
            description=description,
            completion_status=False
        )
        self._storage[new_item.id] = new_item
        self._next_id += 1
        return new_item

    def get_by_id(self, item_id: int) -> Optional[TodoItem]:
        """
        Retrieve a todo item by its ID.

        Args:
            item_id (int): ID of the todo item to retrieve

        Returns:
            TodoItem: The todo item if found, None otherwise
        """
        return self._storage.get(item_id)

    def get_all(self) -> List[TodoItem]:
        """
        Retrieve all todo items.

        Returns:
            List[TodoItem]: List of all todo items in the repository
        """
        return list(self._storage.values())

    def update(self, item_id: int, title: str = None, description: str = None,
               completion_status: bool = None) -> Optional[TodoItem]:
        """
        Update an existing todo item.

        Args:
            item_id (int): ID of the todo item to update
            title (str): New title (optional)
            description (str): New description (optional)
            completion_status (bool): New completion status (optional)

        Returns:
            TodoItem: The updated todo item if found, None otherwise
        """
        if item_id not in self._storage:
            return None

        item = self._storage[item_id]

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title is required and cannot be empty or whitespace only")
            item.title = title.strip()

        if description is not None:
            item.description = description.strip() if description else ""

        if completion_status is not None:
            item.completion_status = completion_status

        return item

    def delete(self, item_id: int) -> bool:
        """
        Delete a todo item by its ID.

        Args:
            item_id (int): ID of the todo item to delete

        Returns:
            bool: True if the item was deleted, False if it didn't exist
        """
        if item_id in self._storage:
            del self._storage[item_id]
            return True
        return False

    def toggle_completion(self, item_id: int) -> Optional[TodoItem]:
        """
        Toggle the completion status of a todo item.

        Args:
            item_id (int): ID of the todo item to toggle

        Returns:
            TodoItem: The updated todo item if found, None otherwise
        """
        if item_id not in self._storage:
            return None

        item = self._storage[item_id]
        item.completion_status = not item.completion_status
        return item

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new todo item.

        Returns:
            int: The next available ID
        """
        return self._next_id