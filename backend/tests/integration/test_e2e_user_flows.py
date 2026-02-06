"""
End-to-end tests for the Todo Application.
Tests complete user workflows from authentication through task management.
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.task_routes import get_current_user_id


@pytest.fixture
def authenticated_client():
    """
    Fixture that provides a test client with authentication set up.
    """
    client = TestClient(app)
    return client


def test_complete_user_workflow():
    """
    Test a complete user workflow: authenticate, create tasks, update, complete, and delete.
    """
    client = TestClient(app)
    user_id = "e2e-test-user-001"

    # Override authentication
    app.dependency_overrides[get_current_user_id] = lambda: user_id

    # Step 1: Create multiple tasks
    task1_data = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=task1_data)
    assert response.status_code == 201
    task1 = response.json()
    assert task1["title"] == "Buy groceries"
    assert task1["completed"] is False
    task1_id = task1["id"]

    task2_data = {
        "title": "Finish project report",
        "description": "Complete sections 3 and 4",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=task2_data)
    assert response.status_code == 201
    task2 = response.json()
    task2_id = task2["id"]

    # Step 2: List all tasks
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2
    assert any(t["id"] == task1_id for t in tasks)
    assert any(t["id"] == task2_id for t in tasks)

    # Step 3: Get a specific task
    response = client.get(f"/api/{user_id}/tasks/{task1_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task1_id
    assert task["title"] == "Buy groceries"

    # Step 4: Update a task
    update_data = {
        "title": "Buy groceries and snacks",
        "description": "Milk, eggs, bread, chips",
        "completed": False
    }
    response = client.put(f"/api/{user_id}/tasks/{task1_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Buy groceries and snacks"
    assert updated_task["description"] == "Milk, eggs, bread, chips"

    # Step 5: Mark task as completed
    response = client.patch(f"/api/{user_id}/tasks/{task1_id}/complete")
    assert response.status_code == 200
    completed_task = response.json()
    assert completed_task["completed"] is True

    # Step 6: Toggle completion back to incomplete
    response = client.patch(f"/api/{user_id}/tasks/{task1_id}/complete")
    assert response.status_code == 200
    incomplete_task = response.json()
    assert incomplete_task["completed"] is False

    # Step 7: Delete a task
    response = client.delete(f"/api/{user_id}/tasks/{task2_id}")
    assert response.status_code == 204

    # Step 8: Verify task was deleted
    response = client.get(f"/api/{user_id}/tasks/{task2_id}")
    assert response.status_code == 404

    # Step 9: Verify remaining tasks
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200
    remaining_tasks = response.json()
    assert any(t["id"] == task1_id for t in remaining_tasks)
    assert not any(t["id"] == task2_id for t in remaining_tasks)

    # Clean up
    app.dependency_overrides.clear()


def test_multi_user_concurrent_operations():
    """
    Test that multiple users can perform operations concurrently without interference.
    """
    client = TestClient(app)
    user1_id = "e2e-user-001"
    user2_id = "e2e-user-002"

    # User 1 creates tasks
    app.dependency_overrides[get_current_user_id] = lambda: user1_id
    user1_task = {
        "title": "User 1 Task",
        "description": "This belongs to user 1",
        "completed": False
    }
    response = client.post(f"/api/{user1_id}/tasks", json=user1_task)
    assert response.status_code == 201
    user1_task_id = response.json()["id"]

    # User 2 creates tasks
    app.dependency_overrides[get_current_user_id] = lambda: user2_id
    user2_task = {
        "title": "User 2 Task",
        "description": "This belongs to user 2",
        "completed": False
    }
    response = client.post(f"/api/{user2_id}/tasks", json=user2_task)
    assert response.status_code == 201
    user2_task_id = response.json()["id"]

    # Verify User 1 only sees their tasks
    app.dependency_overrides[get_current_user_id] = lambda: user1_id
    response = client.get(f"/api/{user1_id}/tasks")
    assert response.status_code == 200
    user1_tasks = response.json()
    assert any(t["id"] == user1_task_id for t in user1_tasks)
    assert not any(t["id"] == user2_task_id for t in user1_tasks)

    # Verify User 2 only sees their tasks
    app.dependency_overrides[get_current_user_id] = lambda: user2_id
    response = client.get(f"/api/{user2_id}/tasks")
    assert response.status_code == 200
    user2_tasks = response.json()
    assert any(t["id"] == user2_task_id for t in user2_tasks)
    assert not any(t["id"] == user1_task_id for t in user2_tasks)

    # Clean up
    app.dependency_overrides.clear()


def test_input_validation_and_error_handling():
    """
    Test that the API properly validates input and returns appropriate error messages.
    """
    client = TestClient(app)
    user_id = "e2e-validation-user"

    app.dependency_overrides[get_current_user_id] = lambda: user_id

    # Test 1: Empty title should fail
    invalid_task = {
        "title": "",
        "description": "This should fail",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=invalid_task)
    assert response.status_code == 400

    # Test 2: Title with only whitespace should fail
    invalid_task = {
        "title": "   ",
        "description": "This should also fail",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=invalid_task)
    assert response.status_code == 400

    # Test 3: Valid task should succeed
    valid_task = {
        "title": "Valid Task",
        "description": "This should work",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=valid_task)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Test 4: Accessing non-existent task should return 404
    response = client.get(f"/api/{user_id}/tasks/non-existent-id")
    assert response.status_code == 404

    # Test 5: Updating non-existent task should return 404
    response = client.put(f"/api/{user_id}/tasks/non-existent-id", json=valid_task)
    assert response.status_code == 404

    # Test 6: Deleting non-existent task should return 404
    response = client.delete(f"/api/{user_id}/tasks/non-existent-id")
    assert response.status_code == 404

    # Clean up
    app.dependency_overrides.clear()


def test_task_completion_toggle():
    """
    Test that task completion status can be toggled multiple times.
    """
    client = TestClient(app)
    user_id = "e2e-toggle-user"

    app.dependency_overrides[get_current_user_id] = lambda: user_id

    # Create a task
    task_data = {
        "title": "Toggle Test Task",
        "description": "Testing completion toggle",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Toggle to completed
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Toggle back to incomplete
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is False

    # Toggle to completed again
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Clean up
    app.dependency_overrides.clear()


def test_task_update_partial_fields():
    """
    Test that tasks can be updated with partial data (only some fields).
    """
    client = TestClient(app)
    user_id = "e2e-partial-update-user"

    app.dependency_overrides[get_current_user_id] = lambda: user_id

    # Create a task
    task_data = {
        "title": "Original Title",
        "description": "Original Description",
        "completed": False
    }
    response = client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Update only the title
    update_data = {
        "title": "Updated Title"
    }
    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Title"
    assert updated_task["description"] == "Original Description"
    assert updated_task["completed"] is False

    # Update only the description
    update_data = {
        "description": "Updated Description"
    }
    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Title"
    assert updated_task["description"] == "Updated Description"

    # Clean up
    app.dependency_overrides.clear()
