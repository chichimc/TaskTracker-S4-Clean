# tests/tasks/test_delete_task.py
import pytest
from app.main import app
from app.services.task_storage import save_tasks
def test_delete_task_success(client):
    """
    Test Case: TC-US007-001
    Purpose: Delete an existing task using a valid ID.

    Scenario:
    - Add a task via POST.
    - Send DELETE to /api/tasks/1.
    - Expect 200 OK with confirmation message: "Task deleted".
    """
    client.post("/api/tasks", json={"title": "Delete Me"})
    response = client.delete("/api/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted"


def test_delete_task_not_found(client):
    """
    Test Case: TC-US007-002
    Purpose: Attempt to delete a task that does not exist.

    Scenario:
    - Send DELETE to /api/tasks/999 (nonexistent ID).
    - Expect 404 Not Found with an error message in response body.
    """
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
    assert "error" in response.get_json()