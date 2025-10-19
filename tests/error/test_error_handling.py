# tests/error/test_error_handling.py

import pytest
from app.main import app

def test_invalid_json_returns_400(client):
    """
    Test Case: TC-US015-001
    Purpose: Ensure server returns 400 Bad Request for malformed JSON payloads.

    Scenario:
    - Send a non-JSON string (not a dict) with content_type="application/json".
    - Flask should detect a parsing error and return a structured 400 error.
    """
    response = client.post("/api/tasks", data="invalid", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_missing_title_returns_400(client):
    """
    Test Case: TC-US015-002
    Purpose: Ensure the API rejects requests missing the required 'title' field.

    Scenario:
    - Send a valid JSON object without the 'title' field.
    - Server should detect the missing field and return a validation error.
    """
    response = client.post("/api/tasks", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_task_not_found_returns_404(client):
    """
    Test Case: TC-US015-003
    Purpose: Ensure a 404 Not Found response is returned for operations on nonexistent tasks.

    Scenario:
    - Attempt to mark a task as complete using an invalid ID (e.g., 999).
    - Server should return 404 and a clear error message.
    """
    response = client.put("/api/tasks/999")
    assert response.status_code == 404
    assert "error" in response.get_json()
