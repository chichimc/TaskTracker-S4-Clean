# tests/task/test_task_service_delete_integration.py
# Integration tests for TaskService.delete_task() with Task class (RF004)

import pytest
from app.services.task_service import TaskService
from app.models.task import Task


def test_delete_task_removes_task_integration(in_memory_repo):
    """
    TC-RF004-004 (integration)
    Integration test for TaskService.delete_task() with Task object refactor
    """
    service = TaskService(storage=in_memory_repo)
    task1 = service.add_task("Task1", "Grocery")
    task2 = service.add_task("Task2", "Study")
    task3 = service.add_task("Task3", "Exercise")

    # Delete Task2 (id=2)
    deleted = service.delete_task(task2["id"])

    assert isinstance(deleted, dict)
    assert deleted["id"] == task2["id"]
    assert deleted["title"] == "Task2"

    # Verify the remaining tasks by fetching from the service
    all_tasks = service.get_all_tasks()

    # Assert remaining tasks
    titles = [t["title"] for t in all_tasks]
    assert "Task2" not in titles
    assert "Task1" in titles
    assert "Task3" in titles
    assert len(all_tasks) == 2


def test_delete_task_returns_none_for_invalid_id_integration(in_memory_repo):
    """
    TC-RF004-004 (integration)
    Integration test for TaskService.delete_task() with invalid ID (Task object refactor)
    """
    service = TaskService(storage=in_memory_repo)
    service.add_task("Task1", "Grocery")

    result = service.delete_task(999)

    assert result is None

    # Verify the valid task remains
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0]["title"] == "Task1"