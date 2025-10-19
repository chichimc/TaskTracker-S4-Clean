# tests/tasks/test_task_model.py
import pytest
from app.models.task import Task  # (assuming Task class will reside in app/models/)

def test_task_instantiation():
    """TC-RF004-001/003: Task object instantiates with correct fields"""
    task = Task(task_id=1, title="Write tests", description="Write unit tests for Task", completed=False)
    assert task.id == 1
    assert task.title == "Write tests"
    assert task.description == "Write unit tests for Task"
    assert task.completed is False

def test_task_default_completed_false():
    """TC-RF004-002: Task.completed defaults to False and can be marked complete"""
    task = Task(task_id=2, title="Do homework", description="Math exercises")
    # By default, completed should be False
    assert task.completed is False

    # Mark the task as complete
    task.mark_complete()  
    # Now completed should be True
    assert task.completed is True

    # Marking an already completed task should keep it True (idempotent)
    task.mark_complete()
    assert task.completed is True