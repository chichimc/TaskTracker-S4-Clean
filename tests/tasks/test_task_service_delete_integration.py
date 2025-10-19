# tests/task/test_task_service_delete_integration.py
# Integration tests for TaskService.delete_task() with Task class (RF004)

import pytest
from app.services.task_service import TaskService
from app.models.task import Task

def test_delete_task_removes_task_integration():
    """
    TC-RF004-004 (integration)
    Integration test for TaskService.delete_task() with Task object refactor
    """
    service = TaskService(storage=None)
    service.add_task("Task1", "Grocery")
    service.add_task("Task2", "Study")
    service.add_task("Task3", "Exercise")
    # Delete Task2 (id=2)
    deleted = service.delete_task(2)
    assert isinstance(deleted, dict)
    assert deleted["id"] == 2
    assert deleted["title"] == "Task2"
    # Internal: _tasks should not contain Task2
    ids = [t.id for t in service._tasks]
    assert 2 not in ids
    assert len(service._tasks) == 2
    # get_all_tasks should not return Task2
    all_tasks = service.get_all_tasks()
    titles = [t["title"] for t in all_tasks]
    assert "Task2" not in titles
    assert "Task1" in titles
    assert "Task3" in titles

def test_delete_task_returns_none_for_invalid_id_integration():
    """
    TC-RF004-004 (integration)
    Integration test for TaskService.delete_task() with invalid ID (Task object refactor)
    """
    service = TaskService(storage=None)
    service.add_task("Task1", "Grocery")
    result = service.delete_task(999)
    assert result is None
    # Internal: _tasks should remain unchanged
    assert len(service._tasks) == 1
    assert service._tasks[0].title == "Task1"
