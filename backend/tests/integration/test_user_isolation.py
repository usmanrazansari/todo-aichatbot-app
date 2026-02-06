import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.task_routes import get_current_user_id


@pytest.fixture
def test_client():
    """Test client for the FastAPI application."""
    return TestClient(app)


def test_user_can_only_access_their_own_tasks():
    """Test that users can only access tasks that belong to them."""
    client = TestClient(app)

    # Mock user IDs for testing
    user1_id = "user1-test-id"
    user2_id = "user2-test-id"

    # Mock task data
    user1_task_data = {
        "title": "User 1 Task",
        "description": "This belongs to user 1",
        "completed": False
    }

    user2_task_data = {
        "title": "User 2 Task",
        "description": "This belongs to user 2",
        "completed": False
    }

    # Override dependency to return user1_id
    app.dependency_overrides[get_current_user_id] = lambda: user1_id

    # User 1 creates a task
    response = client.post(f"/api/{user1_id}/tasks", json=user1_task_data)
    assert response.status_code == 201

    # User 1 should be able to access their own task
    response = client.get(f"/api/{user1_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    assert any(task["title"] == "User 1 Task" for task in tasks)

    # Override dependency to return user2_id
    app.dependency_overrides[get_current_user_id] = lambda: user2_id

    # User 2 creates a task
    response = client.post(f"/api/{user2_id}/tasks", json=user2_task_data)
    assert response.status_code == 201

    # User 2 should be able to access their own task
    response = client.get(f"/api/{user2_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    assert any(task["title"] == "User 2 Task" for task in tasks)

    # User 2 should NOT be able to access User 1's tasks
    response = client.get(f"/api/{user1_id}/tasks")
    assert response.status_code == 403

    # Clean up
    app.dependency_overrides.clear()


def test_user_cannot_modify_other_users_tasks():
    """Test that users cannot modify tasks that don't belong to them."""
    client = TestClient(app)

    # Mock user IDs
    user1_id = "user1-test-id"
    user2_id = "user2-test-id"

    task_data = {
        "title": "Shared Task?",
        "description": "This should not be accessible to others",
        "completed": False
    }

    # User 1 creates a task
    app.dependency_overrides[get_current_user_id] = lambda: user1_id
    response = client.post(f"/api/{user1_id}/tasks", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # User 2 tries to modify User 1's task (should fail)
    app.dependency_overrides[get_current_user_id] = lambda: user2_id
    update_data = {"title": "Hacked by User 2", "completed": True}
    response = client.put(f"/api/{user1_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 403

    # Clean up
    app.dependency_overrides.clear()


def test_user_cannot_delete_other_users_tasks():
    """Test that users cannot delete tasks that don't belong to them."""
    client = TestClient(app)

    # Mock user IDs
    user1_id = "user1-test-id"
    user2_id = "user2-test-id"

    task_data = {
        "title": "Protected Task",
        "description": "This should not be deletable by others",
        "completed": False
    }

    # User 1 creates a task
    app.dependency_overrides[get_current_user_id] = lambda: user1_id
    response = client.post(f"/api/{user1_id}/tasks", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # User 2 tries to delete User 1's task (should fail)
    app.dependency_overrides[get_current_user_id] = lambda: user2_id
    response = client.delete(f"/api/{user1_id}/tasks/{task_id}")
    assert response.status_code == 403

    # Clean up
    app.dependency_overrides.clear()


def test_user_id_validation_in_url_matches_token():
    """Test that the user ID in the URL must match the user ID in the token."""
    client = TestClient(app)

    user1_id = "user1-test-id"
    user2_id = "user2-test-id"

    # User 1 authenticates (has user1_id in token)
    app.dependency_overrides[get_current_user_id] = lambda: user1_id

    # User 1 tries to access user2's tasks (different ID in URL than token)
    response = client.get(f"/api/{user2_id}/tasks")
    assert response.status_code == 403

    # Clean up
    app.dependency_overrides.clear()