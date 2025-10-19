# tests/tasks/test_task_service_get.py
import pytest
from app.services.task_service import TaskService


def test_get_tasks_when_none_exist(in_memory_repo):
    """
    TC-US003-001 / TC-RF005-002 (edge case)
    Unit test for TaskService.get_tasks() when no tasks exist
    Similar to TC-US003-001 but testing service layer directly

    Requirement: TaskService.get_tasks() Returns Task List
    - Expected: List of task objects returned (empty list when no tasks)
    """
    # Arrange
    service = TaskService(storage=in_memory_repo)

    # Act - Get tasks when none exist
    tasks = service.get_tasks()

    # Assert - Should return empty list
    assert isinstance(tasks, list), "get_tasks() should return a list"
    assert tasks == [], "Should return empty list when no tasks exist"


def test_get_tasks_returns_added_tasks(in_memory_repo):
    """
    TC-US003-002 / TC-RF005-002
    Unit test for TaskService.get_tasks() after adding tasks
    Similar to TC-US003-002 but testing service layer directly

    Requirement: TaskService.get_tasks() Returns Task List
    - Description: get_tasks() returns full list of tasks
    - Preconditions: Service has multiple tasks
    - Expected: List of task objects returned
    """
    # Arrange
    service = TaskService(storage=in_memory_repo)

    # Act - Add tasks first
    task1 = service.add_task("Task1", "Grocery")
    task2 = service.add_task("Task2", "Study")

    # Get all tasks
    all_tasks = service.get_tasks()

    # Assert - Should return list with both tasks
    assert isinstance(all_tasks, list), "get_tasks() should return a list"
    assert len(all_tasks) >= 2, "Should return at least two tasks"

    # Check that specific titles are present
    titles = [task["title"] for task in all_tasks]
    assert "Task1" in titles, "Task1 should be in the returned tasks"
    assert "Task2" in titles, "Task2 should be in the returned tasks"

    # Verify task structure
    for task in all_tasks:
        assert "id" in task, "Each task should have an id"
        assert "title" in task, "Each task should have a title"
        assert "description" in task, "Each task should have a description"
        assert "completed" in task, "Each task should have a completed field"