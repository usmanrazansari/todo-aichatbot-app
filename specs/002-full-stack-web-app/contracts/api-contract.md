# API Contract: Todo Application REST API

## Overview
REST API for managing todo tasks in a multi-user environment with JWT authentication.

## Base URL
`http://localhost:8000` (development) or `https://[production-url]`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### GET /api/{user_id}/tasks
Retrieve all tasks for a specific user.

**Path Parameters**:
- `user_id` (string, required): The ID of the user whose tasks to retrieve

**Headers**:
- `Authorization` (string, required): JWT token

**Response**:
- `200 OK`: Array of task objects
```json
[
  {
    "id": "task-uuid-string",
    "user_id": "user-uuid-string",
    "title": "Task title",
    "description": "Task description (optional)",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

### POST /api/{user_id}/tasks
Create a new task for a specific user.

**Path Parameters**:
- `user_id` (string, required): The ID of the user to create the task for

**Headers**:
- `Authorization` (string, required): JWT token

**Request Body**:
```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "completed": false
}
```

**Response**:
- `201 Created`: Created task object
```json
{
  "id": "task-uuid-string",
  "user_id": "user-uuid-string",
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in path doesn't match authenticated user

### GET /api/{user_id}/tasks/{id}
Retrieve a specific task for a user.

**Path Parameters**:
- `user_id` (string, required): The ID of the user
- `id` (string, required): The ID of the task to retrieve

**Headers**:
- `Authorization` (string, required): JWT token

**Response**:
- `200 OK`: Task object
```json
{
  "id": "task-uuid-string",
  "user_id": "user-uuid-string",
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in path doesn't match authenticated user
- `404 Not Found`: Task not found

### PUT /api/{user_id}/tasks/{id}
Update a specific task for a user.

**Path Parameters**:
- `user_id` (string, required): The ID of the user
- `id` (string, required): The ID of the task to update

**Headers**:
- `Authorization` (string, required): JWT token

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description (optional)",
  "completed": true
}
```

**Response**:
- `200 OK`: Updated task object
```json
{
  "id": "task-uuid-string",
  "user_id": "user-uuid-string",
  "title": "Updated task title",
  "description": "Updated task description (optional)",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in path doesn't match authenticated user
- `404 Not Found`: Task not found

### DELETE /api/{user_id}/tasks/{id}
Delete a specific task for a user.

**Path Parameters**:
- `user_id` (string, required): The ID of the user
- `id` (string, required): The ID of the task to delete

**Headers**:
- `Authorization` (string, required): JWT token

**Response**:
- `204 No Content`: Task successfully deleted
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in path doesn't match authenticated user
- `404 Not Found`: Task not found

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle the completion status of a specific task.

**Path Parameters**:
- `user_id` (string, required): The ID of the user
- `id` (string, required): The ID of the task to update

**Headers**:
- `Authorization` (string, required): JWT token

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
- `200 OK`: Updated task object with new completion status
```json
{
  "id": "task-uuid-string",
  "user_id": "user-uuid-string",
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in path doesn't match authenticated user
- `404 Not Found`: Task not found

## Error Responses

All error responses follow this structure:
```json
{
  "detail": "Human-readable error message"
}
```

## Security Considerations
- All endpoints require valid JWT authentication
- User ID in path must match authenticated user ID
- Users can only access their own tasks
- JWT tokens must be validated server-side before processing requests