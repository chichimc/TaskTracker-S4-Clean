# app/repositories/database_task_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.sqlalchemy_task import Task


class TaskRepository(ABC):
    """Abstract base class for task repositories.

    This interface defines the contract that all task repositories must implement,
    allowing different storage backends (file, database, etc.) to be used
    interchangeably.
    """

    @abstractmethod
    def load_tasks(self):
        """Load all tasks from storage.

        Returns:
            List[dict]: List of task dictionaries
        """
        pass

    @abstractmethod
    def save_tasks(self, tasks):
        """Save tasks to storage.

        Args:
            tasks (List[dict]): List of task dictionaries to save
        """
        pass

    @abstractmethod
    def add_task(self, title: str, description: Optional[str] = None):
        """Add a new task to the repository.

        Args:
            title (str): The task title
            description (str, optional): The task description

        Returns:
            Task: The created task object
        """
        pass

    @abstractmethod
    def get_all_tasks(self):
        """Get all tasks from the repository.

        Returns:
            List: List of all tasks
        """
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: int):
        """Get a task by its ID.

        Args:
            task_id (int): The task ID

        Returns:
            Task: The task object if found, None otherwise
        """
        pass

    @abstractmethod
    def update_task(self, task_id: int, **kwargs):
        """Update a task in the repository.

        Args:
            task_id (int): The task ID
            **kwargs: Fields to update

        Returns:
            Task: The updated task object if found, None otherwise
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int):
        """Delete a task from the repository.

        Args:
            task_id (int): The task ID

        Returns:
            bool: True if task was deleted, False if not found
        """
        pass


class DatabaseTaskRepository(TaskRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def load_tasks(self):
        """Load all tasks as dictionaries (for compatibility with TaskService)."""
        session = self.session_factory()
        try:
            tasks = session.query(Task).all()
            return [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed
                }
                for task in tasks
            ]
        finally:
            session.close()

    def save_tasks(self, tasks):
        """Save tasks from a list of dictionaries (for compatibility with TaskService).
        Note: This method recreates all tasks - use carefully.
        """
        session = self.session_factory()
        try:
            # Clear existing tasks
            session.query(Task).delete()
            # Add new tasks
            for task_dict in tasks:
                task = Task(
                    id=task_dict.get('id'),
                    title=task_dict['title'],
                    description=task_dict.get('description'),
                    completed=task_dict.get('completed', False)
                )
                session.add(task)
            session.commit()
        finally:
            session.close()

    def add_task(self, title: str, description: Optional[str] = None):
        """Add a new task to the database."""
        session = self.session_factory()
        try:
            task = Task(title=title, description=description)
            session.add(task)
            session.commit()
            return task
        finally:
            session.close()

    def get_all_tasks(self):
        """Get all tasks from the database."""
        session = self.session_factory()
        try:
            return session.query(Task).all()
        finally:
            session.close()

    def get_task_by_id(self, task_id):
        """Get a task by its ID."""
        session = self.session_factory()
        try:
            return session.query(Task).filter(Task.id == task_id).first()
        finally:
            session.close()

    def update_task(self, task_id, **kwargs):
        """Update a task in the database."""
        session = self.session_factory()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                session.commit()
            return task
        finally:
            session.close()

    def delete_task(self, task_id):
        """Delete a task from the database."""
        session = self.session_factory()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
        finally:
            session.close()