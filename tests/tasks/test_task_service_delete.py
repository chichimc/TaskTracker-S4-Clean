# test/tasks/test_task_service_delete.py

import pytest
from app.services.task_service import TaskService


def test_delete_task_success(in_memory_repo):
    """
    TC-US007-001 / TC-RF005-004
    Unit test for TaskService.delete_task() with valid task ID

    Requirement: TaskService.delete_task() Removes Task
    - Description: delete_task() deletes task with valid ID
    - Preconditions: Task exists
    - Expected: Task is removed from list
    """
    # Arrange
    service = TaskService(storage=in_memory_repo)

    # Add a task first
    new_task = service.add_task("Delete Me", "Task to be deleted")
    task_id = new_task["id"]

    # Verify task exists
    all_tasks_before = service.get_all_tasks()
    assert len(all_tasks_before) == 1
    assert any(task["id"] == task_id for task in all_tasks_before)

    # Act - Delete the task
    deleted_task = service.delete_task(task_id)

    # Assert - Task should be returned and removed from storage
    assert deleted_task is not None, "delete_task should return the deleted task"
    assert deleted_task["id"] == task_id, "Returned task should have the correct ID"
    assert deleted_task["title"] == "Delete Me", "Returned task should have the correct title"
    assert deleted_task["description"] == "Task to be deleted", "Returned task should have the correct description"

    # Verify the task is removed from storage
    all_tasks_after = service.get_all_tasks()
    assert len(all_tasks_after) == 0, "Task should be removed from storage"
    assert not any(task["id"] == task_id for task in all_tasks_after), "Deleted task should not exist in storage"


def test_delete_task_not_found(in_memory_repo):
    """
    TC-US007-002
    Unit test for TaskService.delete_task() with non-existent task ID
    """
    # Arrange
    service = TaskService(storage=in_memory_repo)

    # Act - Try to delete a non-existent task
    result = service.delete_task(999)

    # Assert - Should return None for non-existent task
    assert result is None, "delete_task should return None for non-existent task ID"


def test_delete_task_from_multiple_tasks(in_memory_repo):
    """
    TC-US007-003
    Unit test for TaskService.delete_task() when multiple tasks exist
    """
    # Arrange
    service = TaskService(storage=in_memory_repo)

    # Add multiple tasks
    task1 = service.add_task("Keep Me", "This task should remain")
    task2 = service.add_task("Delete Me", "This task should be deleted")
    task3 = service.add_task("Also Keep", "This task should also remain")

    # Verify all tasks exist
    all_tasks_before = service.get_all_tasks()
    assert len(all_tasks_before) == 3

    # Act - Delete the middle task
    deleted_task = service.delete_task(task2["id"])

    # Assert - Only the correct task should be deleted
    assert deleted_task is not None, "Should return the deleted task"
    assert deleted_task["id"] == task2["id"], "Should return the correct deleted task"

    # Verify remaining tasks are still there
    all_tasks_after = service.get_all_tasks()
    assert len(all_tasks_after) == 2, "Should have 2 tasks remaining"

    remaining_ids = [task["id"] for task in all_tasks_after]
    assert task1["id"] in remaining_ids, "First task should still exist"
    assert task3["id"] in remaining_ids, "Third task should still exist"
    assert task2["id"] not in remaining_ids, "Deleted task should not exist"


def test_delete_already_deleted_task(in_memory_repo):
    """
    TC-US007-004
    Unit test for TaskService.delete_task() on already deleted task
    """
    # Arrange
    service = TaskService(storage=in_memory_repo)

    # Add and delete a task
    new_task = service.add_task("Delete Twice", "Try to delete this twice")
    task_id = new_task["id"]
    service.delete_task(task_id)  # First deletion

    # Act - Try to delete the same task again
    result = service.delete_task(task_id)

    # Assert - Should return None since task no longer exists
    assert result is None, "Should return None when trying to delete already deleted task"