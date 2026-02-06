"""
Command-Line Interface for the Todo application.

Provides the main CLI loop and user interaction functionality.
"""


from typing import Optional
from .service import TodoService
from .validation import validate_title


class TodoAppCLI:
    """
    Main CLI interface for the Todo application.
    Handles user input and interaction with the TodoService.
    """

    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()
        self.running = True

    def run(self):
        """Start the main CLI loop."""
        print("Todo Application Started!")
        print("Type 'help' for available commands or 'quit' to exit.\n")

        while self.running:
            try:
                command = input("Enter command (add/view/update/delete/mark/help/quit): ").strip().lower()
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    def handle_command(self, command: str):
        """Handle a user command."""
        try:
            # Split command to handle commands with arguments
            parts = command.split(' ', 1)
            cmd = parts[0].strip().lower()
            arg = parts[1].strip() if len(parts) > 1 else None

            if cmd in ['quit', 'exit', 'q']:
                self.quit()
            elif cmd in ['help', 'h']:
                self.show_help()
            elif cmd in ['add', 'a']:
                self.add_todo_interactive()
            elif cmd in ['view', 'list', 'v']:
                self.view_todos_interactive()
            elif cmd in ['update', 'u']:
                if arg:
                    self.update_todo_direct(arg)
                else:
                    self.update_todo_interactive()
            elif cmd in ['delete', 'del', 'd']:
                if arg:
                    self.delete_todo_direct(arg)
                else:
                    self.delete_todo_interactive()
            elif cmd in ['mark', 'toggle', 'm']:
                if arg:
                    self.mark_todo_direct(arg)
                else:
                    self.mark_todo_interactive()
            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}\n")

    def quit(self):
        """Quit the application."""
        self.running = False
        print("Goodbye!")

    def show_help(self):
        """Show help information."""
        help_text = """
Available Commands:
  add (a)          - Add a new todo item
  view (v)         - View all todo items
  update (u)       - Update an existing todo item
  delete (d)       - Delete a todo item
  mark (m)         - Mark a todo item as complete/incomplete
  help (h)         - Show this help message
  quit (q)         - Quit the application

Examples:
  add              - Prompts for title and description
  view             - Shows all todos
  update 1         - Updates the todo with ID 1
  delete 1         - Deletes the todo with ID 1
  mark 1           - Toggles completion status of todo with ID 1
"""
        print(help_text)

    def add_todo_interactive(self):
        """Interactive method to add a new todo item."""
        print("\n--- Add New Todo ---")
        try:
            title = input("Enter title: ").strip()

            if not validate_title(title):
                print("Error: Title is required and cannot be empty.\n")
                return

            description = input("Enter description (optional, press Enter to skip): ").strip()
            description = description if description else ""

            new_todo = self.service.add_todo(title, description)
            print(f"Successfully added: [{new_todo.id}] {new_todo.title}\n")

        except Exception as e:
            print(f"Error adding todo: {e}\n")

    def view_todos_interactive(self):
        """Interactive method to view all todo items."""
        print("\n--- All Todos ---")
        todos = self.service.get_all_todos()

        if not todos:
            print("No todos found.\n")
            return

        for todo in todos:
            status = "X" if todo.completion_status else "O"
            print(f"[{status}] {todo.id}. {todo.title}")
            if todo.description:
                print(f"      Description: {todo.description}")
        print()

    def update_todo_interactive(self):
        """Interactive method to update a todo item."""
        print("\n--- Update Todo ---")
        try:
            item_id_input = input("Enter the ID of the todo to update: ").strip()

            if not item_id_input:
                print("Error: Please provide a valid ID.\n")
                return

            try:
                item_id = int(item_id_input)
            except ValueError:
                print("Error: ID must be a number.\n")
                return

            # Check if the item exists
            existing_todo = self.service.get_todo_by_id(item_id)
            if not existing_todo:
                print(f"Error: Todo with ID {item_id} not found.\n")
                return

            print(f"Updating: [{existing_todo.id}] {existing_todo.title}")
            if existing_todo.description:
                print(f"Current description: {existing_todo.description}")

            new_title = input(f"Enter new title (current: '{existing_todo.title}', press Enter to keep current): ").strip()
            if new_title == "":
                new_title = existing_todo.title

            new_description = input(f"Enter new description (current: '{existing_todo.description}', press Enter to keep current): ").strip()
            if new_description == "":
                new_description = existing_todo.description

            updated_todo = self.service.update_todo(item_id, new_title, new_description)
            if updated_todo:
                print(f"Successfully updated: [{updated_todo.id}] {updated_todo.title}\n")
            else:
                print(f"Error: Failed to update todo with ID {item_id}\n")

        except Exception as e:
            print(f"Error updating todo: {e}\n")

    def delete_todo_interactive(self):
        """Interactive method to delete a todo item."""
        print("\n--- Delete Todo ---")
        try:
            item_id_input = input("Enter the ID of the todo to delete: ").strip()

            if not item_id_input:
                print("Error: Please provide a valid ID.\n")
                return

            try:
                item_id = int(item_id_input)
            except ValueError:
                print("Error: ID must be a number.\n")
                return

            # Confirm deletion
            existing_todo = self.service.get_todo_by_id(item_id)
            if not existing_todo:
                print(f"Error: Todo with ID {item_id} not found.\n")
                return

            print(f"You are about to delete: [{existing_todo.id}] {existing_todo.title}")
            confirm = input("Are you sure? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                success = self.service.delete_todo(item_id)
                if success:
                    print(f"Successfully deleted todo with ID {item_id}\n")
                else:
                    print(f"Error: Failed to delete todo with ID {item_id}\n")
            else:
                print("Deletion cancelled.\n")

        except Exception as e:
            print(f"Error deleting todo: {e}\n")

    def mark_todo_interactive(self):
        """Interactive method to toggle completion status of a todo item."""
        print("\n--- Mark Todo ---")
        try:
            item_id_input = input("Enter the ID of the todo to mark: ").strip()

            if not item_id_input:
                print("Error: Please provide a valid ID.\n")
                return

            try:
                item_id = int(item_id_input)
            except ValueError:
                print("Error: ID must be a number.\n")
                return

            self._mark_todo_by_id(item_id)

        except Exception as e:
            print(f"Error marking todo: {e}\n")

    def mark_todo_direct(self, item_id_str: str):
        """Direct method to toggle completion status of a todo item by ID."""
        try:
            try:
                item_id = int(item_id_str)
            except ValueError:
                print("Error: ID must be a number.\n")
                return

            self._mark_todo_by_id(item_id)

        except Exception as e:
            print(f"Error marking todo: {e}\n")

    def _mark_todo_by_id(self, item_id: int):
        """Helper method to toggle completion status of a todo item by ID."""
        existing_todo = self.service.get_todo_by_id(item_id)
        if not existing_todo:
            print(f"Error: Todo with ID {item_id} not found.\n")
            return

        # Toggle the completion status
        updated_todo = self.service.toggle_completion(item_id)
        if updated_todo:
            status = "completed" if updated_todo.completion_status else "pending"
            print(f"Successfully marked todo as {status}: [{updated_todo.id}] {updated_todo.title}\n")
        else:
            print(f"Error: Failed to update todo with ID {item_id}\n")

    def delete_todo_direct(self, item_id_str: str):
        """Direct method to delete a todo item by ID."""
        try:
            try:
                item_id = int(item_id_str)
            except ValueError:
                print("Error: ID must be a number.\n")
                return

            # Check if the item exists
            existing_todo = self.service.get_todo_by_id(item_id)
            if not existing_todo:
                print(f"Error: Todo with ID {item_id} not found.\n")
                return

            print(f"You are about to delete: [{existing_todo.id}] {existing_todo.title}")
            confirm = input("Are you sure? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                success = self.service.delete_todo(item_id)
                if success:
                    print(f"Successfully deleted todo with ID {item_id}\n")
                else:
                    print(f"Error: Failed to delete todo with ID {item_id}\n")
            else:
                print("Deletion cancelled.\n")

        except Exception as e:
            print(f"Error deleting todo: {e}\n")

    def update_todo_direct(self, item_id_str: str):
        """Direct method to update a todo item by ID."""
        try:
            try:
                item_id = int(item_id_str)
            except ValueError:
                print("Error: ID must be a number.\n")
                return

            # Check if the item exists
            existing_todo = self.service.get_todo_by_id(item_id)
            if not existing_todo:
                print(f"Error: Todo with ID {item_id} not found.\n")
                return

            print(f"Updating: [{existing_todo.id}] {existing_todo.title}")
            if existing_todo.description:
                print(f"Current description: {existing_todo.description}")

            new_title = input(f"Enter new title (current: '{existing_todo.title}', press Enter to keep current): ").strip()
            if new_title == "":
                new_title = existing_todo.title

            new_description = input(f"Enter new description (current: '{existing_todo.description}', press Enter to keep current): ").strip()
            if new_description == "":
                new_description = existing_todo.description

            updated_todo = self.service.update_todo(item_id, new_title, new_description)
            if updated_todo:
                print(f"Successfully updated: [{updated_todo.id}] {updated_todo.title}\n")
            else:
                print(f"Error: Failed to update todo with ID {item_id}\n")

        except Exception as e:
            print(f"Error updating todo: {e}\n")


def main():
    """Main entry point for the CLI application."""
    app = TodoAppCLI()
    app.run()


if __name__ == "__main__":
    main()