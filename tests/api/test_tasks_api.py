# tests/api/test_tasks_api.py
import pytest
import requests

BASE_URL = "http://localhost:5000/api/tasks"

def test_add_and_get_tasks_end_to_end():
    """TC-RF008-001/002: Add a task via POST, then retrieve via GET"""
    # 1. Add a new task
    task_data = {"title": "Integration Test Task", "description": "End-to-end test via requests"}
    resp = requests.post(BASE_URL, json=task_data)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] >= 1
    assert created["title"] == "Integration Test Task"
    assert created["description"] == "End-to-end test via requests"
    assert created["completed"] is False

    # 2. Retrieve all tasks and check the new task is present
    resp2 = requests.get(BASE_URL)
    assert resp2.status_code == 200
    tasks = resp2.json()
    # Should contain at least the one we added
    assert isinstance(tasks, list)
    assert any(t["title"] == "Integration Test Task" for t in tasks)
    
def test_complete_task_end_to_end():
  """TC-RF008-003: Complete a task via PUT"""
  # First, create a task to complete
  resp = requests.post(BASE_URL, json={"title": "Task to complete"})
  assert resp.status_code == 201
  task = resp.json()
  task_id = task["id"]
  assert task["completed"] is False

  # Complete the task
  resp2 = requests.put(f"{BASE_URL}/{task_id}")
  assert resp2.status_code == 200
  updated = resp2.json()
  assert updated["id"] == task_id
  assert updated["completed"] is True

  # Verify via GET that the task is now completed
  resp3 = requests.get(BASE_URL)
  tasks = resp3.json()
  completed_task = next((t for t in tasks if t["id"] == task_id), None)
  assert completed_task is not None

def test_delete_task_end_to_end():
    """TC-RF008-004: Delete a task via DELETE"""
    # Create a task to delete
    resp = requests.post(BASE_URL, json={"title": "Task to delete"})
    task_id = resp.json()["id"]

    # Delete the task
    resp2 = requests.delete(f"{BASE_URL}/{task_id}")
    assert resp2.status_code == 200
    result = resp2.json()
    assert result == {"message": "Task deleted"}

    # Verify it's gone
    resp3 = requests.get(BASE_URL)
    tasks = resp3.json()
    ids = [t["id"] for t in tasks]
    assert task_id not in ids

    # Deleting again should yield 404
    resp4 = requests.delete(f"{BASE_URL}/{task_id}")
    assert resp4.status_code == 404
    err = resp4.json()
    assert err["error"] == "Task not found"
