# tests/tasks/test_task_service_complete_integration.py
# Integration tests for TaskService.complete_task() with Task class (RF004)

import pytest
from app.services.task_service import TaskService
from app.models.task import Task


def test_complete_task_marks_task_completed_integration(in_memory_repo):
    """
    TC-RF004-003 (integration)
    Integration test for TaskService.complete_task() with Task object refactor
    """
    service = TaskService(storage=in_memory_repo)

    task1 = service.add_task("Task1", "Grocery")
    task2 = service.add_task("Task2", "Study")

    # Complete Task1
    result = service.complete_task(task1["id"])

    assert isinstance(result, dict)
    assert result["id"] == task1["id"]
    assert result["completed"] is True

    # Verify persistence by fetching the other task's state (indirect check)
    all_tasks = service.get_all_tasks()

    # Check that task 2 (ID 2) is still not completed
    task2_state = next(t for t in all_tasks if t['id'] == task2['id'])
    assert task2_state['completed'] is False


def test_complete_task_returns_none_for_invalid_id_integration(in_memory_repo):
    """
    TC-RF004-003 (integration)
    Integration test for TaskService.complete_task() with invalid ID (Task object refactor)
    """
    service = TaskService(storage=in_memory_repo)

    service.add_task("Task1", "Grocery")
    result = service.complete_task(999)

    assert result is None

    # Verify that the valid task remains unchanged
    all_tasks = service.get_all_tasks()
    assert all_tasks[0]['completed'] is False