# tests/tasks/test_task_service_integration_database.py
# Database integration tests for TaskService (Sprint 4)

import pytest
from flask import current_app


def test_get_tasks_when_none_exist_database_integration(database_client):
    """
    TC-RF004-002 (database integration)
    Integration test for TaskService.get_tasks() when no tasks exist - Database version
    """
    with database_client.application.app_context():
        service = current_app.task_service
        tasks = service.get_tasks()
        assert isinstance(tasks, list)
        assert tasks == []


def test_get_tasks_returns_added_tasks_database_integration(database_client):
    """
    TC-RF004-002 (database integration)
    Integration test for TaskService.get_tasks() after adding tasks - Database version
    """
    with database_client.application.app_context():
        service = current_app.task_service
        task1 = service.add_task("Task1", "Grocery")
        task2 = service.add_task("Task2", "Study")
        all_tasks = service.get_tasks()

        assert isinstance(all_tasks, list)
        assert len(all_tasks) == 2

        # Verify our tasks are there
        titles = [task["title"] for task in all_tasks]
        assert "Task1" in titles
        assert "Task2" in titles


def test_add_task_creates_and_stores_task_database_integration(database_client):
    """
    TC-RF005-001: TaskService.add_task() with database storage
    """
    with database_client.application.app_context():
        service = current_app.task_service
        result = service.add_task("Database Test", "Database description")

        # Check returned structure
        assert isinstance(result, dict)
        assert result["title"] == "Database Test"
        assert result["description"] == "Database description"
        assert result["completed"] is False

        # Verify persistence
        all_tasks = service.get_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0]["title"] == "Database Test"


def test_complete_task_database_integration(database_client):
    """
    Database integration test for task completion
    """
    with database_client.application.app_context():
        service = current_app.task_service
        # Add a task first
        task = service.add_task("Complete me", "Test task")
        task_id = task["id"]

        # Complete it
        completed_task = service.complete_task(task_id)
        assert completed_task is not None
        assert completed_task["completed"] is True

        # Verify persistence
        all_tasks = service.get_tasks()
        assert all_tasks[0]["completed"] is True


def test_delete_task_database_integration(database_client):
    """
    Database integration test for task deletion
    """
    with database_client.application.app_context():
        service = current_app.task_service
        # Add tasks
        task1 = service.add_task("Keep me", "Stay")
        task2 = service.add_task("Delete me", "Go away")

        # Delete one
        deleted = service.delete_task(task2["id"])
        assert deleted is not None

        # Verify only one remains
        all_tasks = service.get_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0]["title"] == "Keep me"