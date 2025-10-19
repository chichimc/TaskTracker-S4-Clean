# app/services/task_service.py
from app.services.task_storage import load_tasks, save_tasks
from app.models.task import Task

# This class encapsulates all task operations (create, read, update, delete) with flexible storage support
class TaskService:
    """Service layer for task management operations.

    🔄 HYBRID ARCHITECTURE PATTERN:
    This class supports both dependency injection AND direct function calls.

    - Unit Tests: Use TaskService(storage=None) → calls load_tasks()/save_tasks() directly
    - Integration: Use TaskService(task_storage) → calls injected storage.load_tasks()/save_tasks()

    📋 NEXT LAB: Once everything works, we'll clean this up to use ONLY dependency injection
    for cleaner, more maintainable code. This hybrid approach is temporary for learning!
    """

    def __init__(self, storage=None):
        self.storage = storage
        # Load tasks from storage and convert to Task objects
        self._tasks = []
        for t in self._load_tasks():
            self._tasks.append(
                Task(
                    t["id"],
                    t["title"],
                    t.get("description", ""),
                    t.get("completed", False),
                )
            )

    def _load_tasks(self):
        """Load tasks using either injected storage or direct functions.
        Returns a list of dicts.
        """
        if self.storage:
            return self.storage.load_tasks()  # Dependency injection path
        return load_tasks()  # Direct function path (for unit tests)

    def _save_tasks(self, tasks):
        """Save tasks using either injected storage or direct functions.
        Accepts a list of dicts.
        """
        if self.storage:
            self.storage.save_tasks(tasks)  # Dependency injection path
        else:
            save_tasks(tasks)  # Direct function path (for unit tests)

    def get_all_tasks(self):
        """Get all tasks from storage (as dicts)."""
        return [t.to_dict() for t in self._tasks]

    def add_task(self, title, description=None):
        """Add a new task with auto-incrementing ID."""
        # Validate title
        if not title or title is None:
            raise ValueError("Title cannot be empty or None")

        # Find the next available ID
        next_id = 1
        if self._tasks:
            next_id = max(task.id for task in self._tasks) + 1

        # Create new Task object
        new_task_obj = Task(
            next_id, title, description if description is not None else "", False
        )
        self._tasks.append(new_task_obj)

        # Save all tasks as dicts
        self._save_tasks([t.to_dict() for t in self._tasks])

        # Return as dict for backward compatibility
        return new_task_obj.to_dict()
    
    def get_tasks(self):
        """Return a list of all tasks (alias for get_all_tasks).
        
        Returns:
            list: List of all task dictionaries
            
        Test Coverage: TC-RF005-002 (Read Tasks)
        """
        # Returns all tasks - same as get_all_tasks()
        return self.get_all_tasks()

    def complete_task(self, task_id):
        """Mark a task as completed.

        Args:
            task_id (int): The ID of the task to complete
        Returns:
            dict: The updated task if found, None if not found
        Test Coverage: TC-RF005-003 (Update Task)
        """
        # IMPORTANT: self._tasks is our in-memory (RAM) list of Task objects.
        # We operate on this list directly for speed and efficiency, instead of reloading from disk (storage) every time.
        # This is how real-world service layers work: keep data in memory, only save to storage when changes are made.
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                # Persist the updated list to storage
                self._save_tasks([t.to_dict() for t in self._tasks])
                return task.to_dict()  # Return as dict for backward compatibility
        return None     

    def delete_task(self, task_id):
        """Delete a task from the system.
        
        Args:
            task_id (int): The ID of the task to delete
        Returns:
            dict: The deleted task if found, None if not found
        Test Coverage: TC-RF005-004 (Delete Task)
        """
        # Real-world: operate on self._tasks (in-memory Task objects), not by reloading from storage.
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                deleted_task = self._tasks.pop(i)
                # Persist the updated list to storage
                self._save_tasks([t.to_dict() for t in self._tasks])
                return deleted_task.to_dict()  # Return as dict for backward compatibility
        return None    

    def clear_tasks(self):
        """Clear all tasks."""
        self._tasks = []
        self._save_tasks([])