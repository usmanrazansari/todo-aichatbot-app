"""
Data models for the Todo application.

Contains the TodoItem class representing a single todo item.
"""


class TodoItem:
    """
    Represents a single todo item with attributes:
    - id: Unique identifier (integer)
    - title: Required title (string)
    - description: Optional description (string)
    - completion_status: Boolean indicating if the item is completed
    """

    def __init__(self, item_id: int, title: str, description: str = "", completion_status: bool = False):
        """
        Initialize a TodoItem instance.

        Args:
            item_id (int): Unique identifier for the todo item
            title (str): Required title of the todo item
            description (str): Optional description of the todo item
            completion_status (bool): Whether the item is completed (default: False)
        """
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty or whitespace only")

        self.id = item_id
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.completion_status = completion_status

    def __repr__(self):
        """Return a string representation of the TodoItem."""
        status = "Completed" if self.completion_status else "Pending"
        return f"TodoItem(id={self.id}, title='{self.title}', description='{self.description}', status={status})"

    def __str__(self):
        """Return a user-friendly string representation of the TodoItem."""
        status = "X" if self.completion_status else "O"
        return f"[{status}] {self.id}. {self.title}"

    def to_dict(self):
        """Convert the TodoItem to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completion_status": self.completion_status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a TodoItem instance from a dictionary."""
        return cls(
            item_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completion_status=data.get("completion_status", False)
        )