# tests/conftest.py

import os
import json
import pytest
import requests
from app import create_app

BASE_URL = "http://localhost:5000/api/tasks"


# Mock service for isolated route tests (keep for unit/mocked tests)
class MockTaskService:
    """Mock implementation of TaskService for testing routes without file I/O."""
    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def get_all_tasks(self):
        return [task.copy() for task in self._tasks]

    def add_task(self, title, description=None):
        title = (title or "").strip()
        if not title:
            raise ValueError("Title is required")
        new_task = {
            "id": self._next_id,
            "title": title,
            "description": description or "",
            "completed": False
        }
        self._tasks.append(new_task)
        self._next_id += 1
        return new_task

    def complete_task(self, task_id):
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return task
        return None

    def delete_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task["id"] == task_id:
                return self._tasks.pop(i)
        return None

    def clear_tasks(self):
        self._tasks = []
        self._next_id = 1

@pytest.fixture
def mock_service():
    return MockTaskService()

# Main app fixture for pytest-flask (session scope for live_server compatibility)
@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

# Flask test client for non-live tests
@pytest.fixture
def client(app):
    return app.test_client()

# 📍 Location of the persistent task file
TASKS_FILE = os.path.join("app", "data", "tasks.json")

# Reset tasks before and after each test (for file-backed service)
@pytest.fixture(autouse=True)
def reset_tasks(client):
    try:
        response = client.post("/api/tasks/reset")
        assert response.status_code == 200
    except Exception:
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)

    yield  # Execute the test

    try:
        client.post("/api/tasks/reset")
    except Exception:
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)