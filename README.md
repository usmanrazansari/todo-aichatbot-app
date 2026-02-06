# Todo Application - In-Memory Console App

A basic command-line Todo application that stores all tasks in memory, demonstrating clean architecture and agentic development workflow.

## Features

- Add new todo items with titles and optional descriptions
- View all todo items with their status
- Update existing todo items
- Delete todo items
- Mark todo items as completed/pending
- In-memory storage (no persistence between runs)

## Requirements

- Python 3.13+

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

Or run directly with:
```bash
uv run main.py
```

## Usage

Run the application:
```bash
python main.py
```

The application provides an interactive command-line interface with the following commands:

- `add` (a) - Add a new todo item
- `view` (v) - View all todo items
- `update` (u) - Update an existing todo item
- `delete` (d) - Delete a todo item
- `mark` (m) - Mark a todo item as complete/incomplete
- `help` (h) - Show help information
- `quit` (q) - Quit the application

### Examples

1. **Adding a new todo:**
   - Type `add` or `a`
   - Enter a title when prompted
   - Optionally enter a description

2. **Viewing all todos:**
   - Type `view` or `v`
   - See all todos with their ID, title, description, and status

3. **Updating a todo:**
   - Type `update` or `u`
   - Enter the ID of the todo to update
   - Follow the prompts to update the title or description

4. **Deleting a todo:**
   - Type `delete` or `d`
   - Enter the ID of the todo to delete
   - Confirm the deletion

5. **Marking a todo:**
   - Type `mark` or `m`
   - Enter the ID of the todo to toggle its completion status

## Architecture

The application follows clean architecture principles:

- **Models**: Data structures (TodoItem)
- **Repository**: In-memory data storage (TodoRepository)
- **Service**: Business logic (TodoService)
- **CLI**: User interface (TodoAppCLI)

## License

MIT