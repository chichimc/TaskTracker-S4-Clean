# test_task_service_add.py 

import pytest
from app.services.task_service import TaskService

def test_add_task_creates_new_task(tmp_path):
    """
    TC-US002-001
    Unit test for TaskService.add_task() creating and persisting new tasks
    """
    service = TaskService(storage=None)
    # Ensure no tasks exist at start
    assert service.get_all_tasks() == []  # should be empty initially
    
    # Add a new task
    new_task = service.add_task("Buy groceries", "Milk and eggs")
    # Check the returned task structure
    assert new_task["id"] == 1  # first task gets ID 1
    assert new_task["title"] == "Buy groceries"
    assert new_task["description"] == "Milk and eggs"
    assert new_task["completed"] is False
    
    # The task should now be persisted in the file
    all_tasks = service.get_all_tasks()
    assert any(task["title"] == "Buy groceries" for task in all_tasks)
    assert all_tasks[0]["id"] == 1  # the list should contain our new task
    
    # Add another task to ensure ID increments
    second_task = service.add_task("Do homework")
    assert second_task["id"] == 2  # now the ID should be 2
    titles = [t["title"] for t in service.get_all_tasks()]
    assert "Do homework" in titles

# TC US002-002 Missing Title
def test_add_task_empty_title():
    """
    TC-US002-002
    Unit test for TaskService.add_task() with empty title
    """
    service = TaskService(storage=None)
    with pytest.raises(ValueError):
        service.add_task("", "No title")

def test_add_task_none_title():
    """
    TC-US002-003
    Unit test for TaskService.add_task() with None title
    """
    service = TaskService(storage=None)
    with pytest.raises(ValueError):
        service.add_task(None, "No title")