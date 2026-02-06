# Implementation Tasks: Todo In-Memory Python Console Application (Phase I)

**Feature**: 001-todo-console-app
**Created**: 2026-02-05
**Status**: Draft

## Phase 1: Setup

Goal: Initialize project structure and environment

**Independent Test**: Run `python main.py` and see basic application startup

- [X] T001 Create project directory structure (main.py, todo_app/, tests/)
- [X] T002 Initialize UV environment with Python 3.13+ requirements
- [X] T003 Create basic project files and __init__.py files

## Phase 2: Foundational

Goal: Establish core architecture with data models and repository layer

**Independent Test**: Import and instantiate TodoItem class successfully

- [X] T004 [P] Create TodoItem data model class with id, title, description, completion_status attributes in todo_app/models.py
- [X] T005 [P] Create TodoRepository in-memory storage with CRUD operations in todo_app/repository.py
- [X] T006 [P] Create TodoService with business logic methods in todo_app/service.py

## Phase 3: User Story 1 - Add New Todo Item (Priority: P1)

Goal: Enable users to add new todo items with unique IDs and pending status

**Independent Test**: Add a new todo item and verify it appears in the system with correct details

**Acceptance**:
- Given I am using the todo application, When I choose to add a new item with a title, Then the item should be created with a unique ID and pending status
- Given I am adding a new item, When I provide both title and description, Then both should be saved correctly
- Given I am adding a new item, When I provide only a title, Then the description should be empty but the item should still be created

- [X] T007 [P] [US1] Implement add_todo method in TodoService with validation for non-empty title
- [X] T008 [P] [US1] Create input validation function for todo items in todo_app/validation.py
- [X] T009 [US1] Add 'Add Todo' option to main menu in main.py
- [X] T010 [US1] Implement CLI handler for adding new todo items in todo_app/cli.py

## Phase 4: User Story 2 - View All Todo Items (Priority: P1)

Goal: Allow users to view all todo items in a clear, readable format

**Independent Test**: Add a few items and view the complete list with all details

**Acceptance**:
- Given I have added one or more todo items, When I choose to view all items, Then all items should be displayed with their ID, title, description, and completion status
- Given I have no todo items, When I choose to view all items, Then an appropriate message should indicate the list is empty

- [X] T011 [P] [US2] Implement get_all_todos method in TodoService
- [X] T012 [US2] Add 'View Todos' option to main menu in main.py
- [X] T013 [US2] Implement CLI handler for displaying all todo items in todo_app/cli.py
- [X] T014 [US2] Create formatting function for displaying todos in readable format in todo_app/formatters.py

## Phase 5: User Story 3 - Mark Todo Item as Completed (Priority: P2)

Goal: Allow users to mark todo items as completed or pending to track progress

**Independent Test**: Mark an item as completed and verify its status changes

**Acceptance**:
- Given I have a pending todo item, When I choose to mark it as completed, Then its status should update to completed
- Given I have a completed todo item, When I choose to mark it as pending again, Then its status should update to pending

- [X] T015 [P] [US3] Implement toggle_completion method in TodoService
- [X] T016 [US3] Add 'Mark Todo Complete/Pending' option to main menu in main.py
- [X] T017 [US3] Implement CLI handler for toggling todo completion status in todo_app/cli.py

## Phase 6: User Story 4 - Update Todo Item Details (Priority: P3)

Goal: Allow users to update title or description of existing todo items

**Independent Test**: Update an item's details and verify the changes are saved

**Acceptance**:
- Given I have an existing todo item, When I choose to update its title or description, Then the changes should be saved and reflected when viewing the item

- [X] T018 [P] [US4] Implement update_todo method in TodoService with validation
- [X] T019 [US4] Add 'Update Todo' option to main menu in main.py
- [X] T020 [US4] Implement CLI handler for updating todo item details in todo_app/cli.py

## Phase 7: User Story 5 - Delete Todo Item (Priority: P3)

Goal: Allow users to delete specific todo items from the list

**Independent Test**: Delete an item and verify it no longer appears in the list

**Acceptance**:
- Given I have one or more todo items, When I choose to delete a specific item, Then that item should be removed from the list

- [X] T021 [P] [US5] Implement delete_todo method in TodoService
- [X] T022 [US5] Add 'Delete Todo' option to main menu in main.py
- [X] T023 [US5] Implement CLI handler for deleting todo items in todo_app/cli.py

## Phase 8: Error Handling and Validation

Goal: Handle edge cases and invalid inputs gracefully

**Independent Test**: Attempt invalid operations and verify application handles them without crashing

- [X] T024 [P] Add validation to handle non-existent todo item IDs
- [X] T025 [P] Implement error handling for empty or whitespace-only titles
- [X] T026 Add error handling for invalid user inputs throughout the application
- [X] T027 Create user-friendly error messages for all error scenarios

## Phase 9: Polish & Cross-Cutting Concerns

Goal: Enhance user experience and finalize application

**Independent Test**: Complete walkthrough of all features with smooth user experience

- [X] T028 Improve menu navigation and user prompts
- [X] T029 Add clear formatting and readability to all console outputs
- [X] T030 Implement graceful shutdown and exit functionality
- [X] T031 Conduct full integration test of all features
- [X] T032 Document the application usage in README.md

## Dependencies

- User Story 1 (Add) and User Story 2 (View) are foundational and should be completed first
- User Stories 3-5 (Mark Complete, Update, Delete) depend on Stories 1-2
- Phase 8 (Error Handling) should be applied after core functionality is implemented

## Parallel Execution Opportunities

- T004-T006: Data model, repository, and service layer can be developed in parallel
- T007, T011, T015, T018, T021: Service methods can be implemented in parallel
- T012, T016, T019, T022: Main menu options can be added in parallel

## Implementation Strategy

- MVP scope: Complete Phase 1, 2, and User Story 1-2 for basic add/view functionality
- Incremental delivery: Add one user story at a time with full end-to-end functionality
- Each phase should result in a working, testable application