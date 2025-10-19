# app/services/task_storage.py
import os
import json

TASKS_FILE = os.path.join("app", "data", "tasks.json")

def load_tasks():
    """Load tasks from the JSON file or return an empty list on failure."""
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """Write the task list to the JSON file, ensuring directory exists."""
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=2)
    except IOError as e:
        print(f"[Warning] Error saving tasks: {e}")
        
# ✅ Phase 2: Dependency Injection Infrastructure
# Class wrapper for DI (enables both old and new patterns)
class TaskStorage:
    """Storage interface for task persistence.
    
    🔄 WRAPPER PATTERN: This class wraps the existing load_tasks/save_tasks functions
    to enable dependency injection while keeping the original functions working.
    
    📋 NEXT LAB: Once all tests pass and we're confident in the DI pattern,
    we can refactor to use ONLY this class and remove the standalone functions
    for cleaner, more object-oriented code.
    """
    
    def load_tasks(self):
        """Load tasks using the underlying load_tasks function."""
        return load_tasks()
    
    def save_tasks(self, tasks):
        """Save tasks using the underlying save_tasks function."""
        save_tasks(tasks)


# ✅ Singleton instance for dependency injection
# This instance will be injected into TaskService in __init__.py
task_storage = TaskStorage()