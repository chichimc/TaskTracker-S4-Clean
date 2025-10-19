# test_task_service_complete_integration.py
# Integration tests for TaskService.complete_task() with Task class (RF004)

import pytest
from app.services.task_service import TaskService
from app.models.task import Task

def test_complete_task_marks_task_completed_integration():
    """
    TC-RF004-003 (integration)
    Integration test for TaskService.complete_task() with Task object refactor
    """
    service = TaskService(storage=None)
    service.add_task("Task1", "Grocery")
    service.add_task("Task2", "Study")
    # Complete Task1
    result = service.complete_task(1)
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["completed"] is True
    # Internal: _tasks should reflect completion
    assert service._tasks[0].completed is True
    assert service._tasks[1].completed is False

def test_complete_task_returns_none_for_invalid_id_integration():
    """
    TC-RF004-003 (integration)
    Integration test for TaskService.complete_task() with invalid ID (Task object refactor)
    """
    service = TaskService(storage=None)
    service.add_task("Task1", "Grocery")
    result = service.complete_task(999)
    assert result is None
    # Internal: _tasks should remain unchanged
    assert service._tasks[0].completed is False
