# tests/tasks/test_get_task.py

import pytest
def test_view_tasks_when_none_exist(client):
    """
    TC-US003-001
    """
    # Act - Immediately retrieve tasks (no POSTs beforehand)
    response = client.get("/api/tasks")

    # Assert - Validate status and empty list
    assert response.status_code == 200, "Should return 200 OK even if no tasks exist"
    data = response.get_json()

    assert isinstance(data, list), "Response should be a list"
    assert data == [], "List should be empty if no tasks exist"

def test_view_all_tasks(client):
    """
    TC-US003-002
    """
    # Setup - Add two tasks using POST requests
    client.post("/api/tasks", json={"title": "Task1", "description": "Grocery"})
    client.post("/api/tasks", json={"title": "Task2", "description": "Study"})

    # Action - Retrieve all tasks using GET
    response = client.get("/api/tasks")

    # Assert - Validate status and response structure
    assert response.status_code == 200, "GET should return 200 OK"
    data = response.get_json()

    assert isinstance(data, list), "Response should be a list"
    assert len(data) >= 2, "Should return at least two tasks"

    # 🔍 Check that specific titles are present
    titles = [task["title"] for task in data]
    assert "Task1" in titles
    assert "Task2" in titles  

def test_invalid_method_on_tasks(client):
    """
    TC-US003-003
    """

    # PUT is not allowed on /api/tasks
    response = client.put("/api/tasks", json={
        "title": "Invalid",
        "description": "Should be disallowed"
    })

    # The response should be 405 Method Not Allowed
    assert response.status_code == 405, "Expected 405 when using unsupported HTTP method"
    
def test_blueprint_routes_accessible(client):
    response = client.get("/api/tasks")
    assert response.status_code in [200, 201]