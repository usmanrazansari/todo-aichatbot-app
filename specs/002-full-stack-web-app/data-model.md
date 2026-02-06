# Data Model: Todo Application – Phase II (Full-Stack Web Application)

## Overview
This document defines the data models for the multi-user todo application, including entity definitions, relationships, and validation rules.

## Entity Definitions

### User
Represents an authenticated user in the system.
Managed by Better Auth, with user ID provided for linking tasks.

**Attributes**:
- `id` (string): Unique identifier provided by Better Auth system
- `email` (string): User's email address for authentication
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last account update timestamp

**Relationships**:
- One-to-many with Task (one user can have many tasks)

### Task
Represents a todo item owned by a specific user.

**Attributes**:
- `id` (UUID/string): Unique identifier for the task
- `user_id` (string): Foreign key linking to the owning user
- `title` (string): Title of the task (required, max 255 characters)
- `description` (string): Optional description of the task (nullable, max 1000 characters)
- `completed` (boolean): Completion status of the task (default: false)
- `created_at` (datetime): Task creation timestamp
- `updated_at` (datetime): Last task update timestamp

**Validation Rules**:
- `title` is required and must be 1-255 characters
- `description`, if provided, must be 1-1000 characters
- `completed` must be a boolean value
- `user_id` must correspond to an existing user

**Relationships**:
- Many-to-one with User (many tasks belong to one user)

## State Transitions

### Task Completion States
- **Pending** (completed: false) → **Completed** (completed: true): When user marks task as complete
- **Completed** (completed: true) → **Pending** (completed: false): When user marks task as incomplete

## Indexes
- Index on `user_id` for efficient retrieval of user-specific tasks
- Index on `completed` status for filtering completed/incomplete tasks
- Combined index on `(user_id, completed)` for optimized user-task queries

## Constraints
- Foreign key constraint: `user_id` in tasks table must reference an existing user
- Check constraint: `title` must not be empty
- Check constraint: `title` length between 1-255 characters