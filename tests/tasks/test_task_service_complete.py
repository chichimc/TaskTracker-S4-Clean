# test/tasks/test_task_service_complete.py
import pytest
from app.services.task_service import TaskService

def test_complete_task_success():
    """
    TC-US005-001 / TC-RF005-003
    Unit test for TaskService.complete_task() with valid task ID
    
    Requirement: TaskService.update_task() Updates Completion Status
    - Description: update_task() updates the completion status of a task
    - Preconditions: Task exists with completed=False
    - Expected: Task is marked as complete
    
    Note: complete_task() implements the update functionality for completion status
    """
    # Arrange
    service = TaskService(storage=None)
    
    # Add a task first
    new_task = service.add_task("Test Task", "Test description")
    task_id = new_task["id"]
    
    # Verify task is initially not completed
    assert new_task["completed"] is False
    
    # Act - Complete the task
    completed_task = service.complete_task(task_id)
    
    # Assert - Task should be marked as completed
    assert completed_task is not None, "complete_task should return the completed task"
    assert completed_task["id"] == task_id, "Returned task should have the correct ID"
    assert completed_task["completed"] is True, "Task should be marked as completed"
    assert completed_task["title"] == "Test Task", "Title should remain unchanged"
    assert completed_task["description"] == "Test description", "Description should remain unchanged"
    
    # Verify the task is persisted as completed
    all_tasks = service.get_all_tasks()
    persisted_task = next((task for task in all_tasks if task["id"] == task_id), None)
    assert persisted_task is not None, "Task should still exist in storage"
    assert persisted_task["completed"] is True, "Task should be persisted as completed"

def test_complete_task_not_found():
    """
    TC-US005-002
    Unit test for TaskService.complete_task() with non-existent task ID
    """
    # Arrange
    service = TaskService(storage=None)
    
    # Act - Try to complete a non-existent task
    result = service.complete_task(999)
    
    # Assert - Should return None for non-existent task
    assert result is None, "complete_task should return None for non-existent task ID"

def test_complete_already_completed_task():
    """
    TC-US005-003
    Unit test for TaskService.complete_task() on already completed task
    """
    # Arrange
    service = TaskService(storage=None)
    
    # Add and complete a task
    new_task = service.add_task("Already done", "Already completed task")
    task_id = new_task["id"]
    service.complete_task(task_id)  # First completion
    
    # Act - Complete the same task again
    result = service.complete_task(task_id)
    
    # Assert - Should still return the task, still marked as completed
    assert result is not None, "Should return the task even if already completed"
    assert result["completed"] is True, "Task should remain completed"
    assert result["id"] == task_id, "Should return the correct task"