"""
Validation utilities for the Todo application.

Contains functions for validating user input.
"""


def validate_title(title: str) -> bool:
    """
    Validate that a title is not empty or whitespace only.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if the title is valid, False otherwise
    """
    if not title or not title.strip():
        return False
    return True


def validate_todo_item(title: str, description: str = "") -> tuple[bool, str]:
    """
    Validate a todo item's attributes.

    Args:
        title (str): The title to validate
        description (str): The description to validate

    Returns:
        tuple[bool, str]: (is_valid, error_message) where is_valid is True if valid,
                         and error_message describes any validation error
    """
    if not validate_title(title):
        return False, "Title is required and cannot be empty or whitespace only"

    # Additional validations can be added here

    return True, ""


def validate_item_id(item_id: str) -> tuple[bool, int, str]:
    """
    Validate that an item ID is a positive integer.

    Args:
        item_id (str): The item ID to validate

    Returns:
        tuple[bool, int, str]: (is_valid, parsed_id, error_message) where is_valid is True if valid,
                              parsed_id is the integer value if valid, and error_message describes any validation error
    """
    try:
        parsed_id = int(item_id)
        if parsed_id <= 0:
            return False, 0, "Item ID must be a positive integer"
        return True, parsed_id, ""
    except ValueError:
        return False, 0, "Item ID must be a valid integer"