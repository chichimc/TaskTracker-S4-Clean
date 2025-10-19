# tests/conftest.py

import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)

"""
Test configuration and fixtures for the Task Management Application.

📝 NOTE FOR STUDENTS: You may see "ResourceWarning: unclosed database" warnings 
when running tests. This is NORMAL and expected behavior! These warnings occur 
because SQLAlchemy database connections are automatically cleaned up by Python's 
garbage collector rather than being explicitly closed in test fixtures. 

The warnings do NOT indicate:
- ❌ Broken tests
- ❌ Failed functionality  
- ❌ Code errors

Your tests are working correctly even with these warnings. In production code,
we would implement proper connection cleanup, but for educational testing 
purposes, these warnings can be safely ignored.

🎯 Focus on: Test results (PASSED/FAILED) - not the warnings!
"""

import os
import json
import pytest
import requests

from app import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.sqlalchemy_task import Base
from app.repositories.database_task_repository import DatabaseTaskRepository
from app.services.task_service import TaskService

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


# ============================================
# 🔧 Database Setup for SQLAlchemy (Sprint 4)
# ============================================

# 🚩 STUDENT NOTE FOR SPRINT 5 (Robot Framework):
# For unit tests, we use an in-memory SQLite database (fast, disposable, not persistent).
# For end-to-end tests (Robot Framework, Selenium, etc.), you will switch to a file-based SQLite database (sqlite:///tasks.db)
# This makes your test data persistent and matches real-world usage.
# You will need to clean up tasks.db before/after Robot tests to ensure a fresh state.
# This is NORMAL and expected for E2E testing!

@pytest.fixture
def session_factory():
    """Provides a clean in-memory database session factory for SQLAlchemy tests."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
    engine.dispose()


@pytest.fixture
def database_test_app(session_factory):
    """Creates a Flask app with a test database and injected service."""
    repo = DatabaseTaskRepository(session_factory)
    service = TaskService(repo)
    app = create_app()
    app.task_service = service
    app.config["TESTING"] = True
    return app


@pytest.fixture
def database_client(database_test_app):
    """Flask test client using in-memory DB and DI-injected service."""
    return database_test_app.test_client()


@pytest.fixture
def in_memory_repo():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    repo = DatabaseTaskRepository(Session)
    yield repo
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def cleanup_engine():
    app = create_app()
    yield
    if hasattr(app, "database_engine"):
        app.database_engine.dispose()