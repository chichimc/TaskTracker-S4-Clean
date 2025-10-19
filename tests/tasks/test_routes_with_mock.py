import pytest
from flask import current_app
from app import create_app
from tests.conftest import MockTaskService

@pytest.fixture()
def app_with_mock():
    # TC-RF008-005
    app = create_app(service=MockTaskService())
    app.config['TESTING'] = True
    return app

def test_add_task_route_uses_service(app_with_mock):
    # TC-RF008-006: Add Task Using MockTaskService
    client = app_with_mock.test_client()
    response = client.post('/api/tasks', json={"title": "Mock Task", "description": "Test DI"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Mock Task"
    assert data["description"] == "Test DI"
    assert data["completed"] is False
    # IMPORTANT FOR BEGINNERS:
    # When testing Flask routes, always use the test client to fetch data.
    # This ensures you see the same state as a real user of the API, and avoids issues with Flask's app/request context.
    # Do NOT access current_app.task_service directly for state checks in route tests.
    tasks_response = client.get('/api/tasks')
    tasks = tasks_response.get_json()
    assert any(task["title"] == "Mock Task" for task in tasks)
    response2 = client.post('/api/tasks', json={"description": "No title here"})
    assert response2.status_code == 400
    error = response2.get_json()
    assert "error" in error and error["error"] == "Title is required"

def test_complete_task_route_with_mock(app_with_mock):
    # TC-RF008-007: Complete Task Using MockTaskService
    client = app_with_mock.test_client()
    # Add a task via the route to ensure it's visible to the test client
    response = client.post('/api/tasks', json={"title": "Finish Lab", "description": "Complete Sprint 3 Lab 2"})
    assert response.status_code == 201
    t = response.get_json()
    task_id = t["id"]
    resp = client.put(f'/api/tasks/{task_id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == task_id
    assert data["completed"] is True
    resp2 = client.put('/api/tasks/999')
    assert resp2.status_code == 404
    err = resp2.get_json()
    assert err["error"] == "Task not found"

def test_delete_task_route_with_mock(app_with_mock):
    #TC-RF008-008: Delete Task Using MockTaskService
    client = app_with_mock.test_client()
    # Add two tasks via the route
    resp1 = client.post('/api/tasks', json={"title": "Task A"})
    assert resp1.status_code == 201
    resp2 = client.post('/api/tasks', json={"title": "Task B"})
    assert resp2.status_code == 201
    t2 = resp2.get_json()
    task_id = t2["id"]
    resp = client.delete(f'/api/tasks/{task_id}')
    assert resp.status_code == 200
    msg = resp.get_json()
    assert msg == {"message": "Task deleted"}
    # Verify that task is actually removed in service
    tasks = client.get('/api/tasks')
    titles = [t["title"] for t in tasks.get_json()]
    assert "Task B" not in titles
    resp2 = client.delete(f'/api/tasks/{task_id}')
    assert resp2.status_code == 404
    err = resp2.get_json()
    assert err["error"] == "Task not found"