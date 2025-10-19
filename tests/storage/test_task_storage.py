# /tests/storage/test_task_storage.py
import pytest
from app.services.task_storage import save_tasks, load_tasks

def test_save_and_load_tasks():
    """Test that tasks can be saved and loaded from the default storage."""
    test_tasks = [{"id": 1, "title": "Persisted Task",  "completed": False}]

    # Clear any existing tasks first
    save_tasks([])

    # Save test tasks
    save_tasks(test_tasks)

    # Load and verify
    loaded_tasks = load_tasks()
    assert loaded_tasks == test_tasks

    # Clean up
    save_tasks([])

def test_load_tasks_empty_file():
    """Test loading tasks when no tasks exist."""
    # Clear tasks to ensure empty state
    save_tasks([])

    loaded_tasks = load_tasks()
    assert loaded_tasks == []