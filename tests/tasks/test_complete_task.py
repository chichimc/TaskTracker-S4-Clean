# tests/tasks/test_complete_task.py
import pytest
from app.main import app

def test_complete_task_success(client):
    """
    Test Case: TC-US005-001
    Purpose: Mark a task as complete using a valid task ID.

    Scenario:
    - Add a task using POST /api/tasks.
    - Send PUT request to /api/tasks/1.
    - Expect 200 OK with updated task including "completed": true and correct ID.
    """
    client.post("/api/tasks", json={"title": "Test Task", "description": "Test"})
    response = client.put("/api/tasks/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["completed"] is True
    assert data["id"] == 1


def test_complete_task_not_found(client):
    """
    Test Case: TC-US005-002
    Purpose: Attempt to complete a non-existent task.

    Scenario:
    - Send PUT request to /api/tasks/999 (non-existent ID).
    - Expect 404 Not Found with an appropriate error message in response body.
    """
    response = client.put("/api/tasks/999")
    assert response.status_code == 404
    assert "error" in response.get_json()