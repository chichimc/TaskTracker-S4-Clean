from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.sqlalchemy_task import Task
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect


class TaskRepository(ABC):
    @abstractmethod
    def load_tasks(self):
        pass

    @abstractmethod
    def save_tasks(self, tasks):
        pass

    @abstractmethod
    def add_task(self, title: str, description: Optional[str] = None):
        pass

    @abstractmethod
    def get_all_tasks(self):
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: int):
        pass

    @abstractmethod
    def update_task(self, task_id: int, **kwargs):
        pass

    @abstractmethod
    def delete_task(self, task_id: int):
        pass

    @abstractmethod
    def clear_tasks(self):
        pass


class DatabaseTaskRepository(TaskRepository):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def load_tasks(self):
        session = self.session_factory()
        try:
            tasks = session.query(Task).all()
            return [task.to_dict() for task in tasks]
        finally:
            session.close()

    def save_tasks(self, tasks: List[dict]):
        session = self.session_factory()
        try:
            session.query(Task).delete()
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
        session = self.session_factory()
        try:
            task = Task(title=title, description=description)
            session.add(task)
            session.flush()
            session.refresh(task)

            task_dict = task.to_dict()

            session.commit()
            return task_dict
        finally:
            session.close()

    def get_all_tasks(self):
        session = self.session_factory()
        try:
            tasks = session.query(Task).all()
            return [task.to_dict() for task in tasks]
        finally:
            session.close()

    def get_task_by_id(self, task_id: int):
        session = self.session_factory()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                return task.to_dict()
            return None
        finally:
            session.close()

    def update_task(self, task_id: int, **kwargs):
        session = self.session_factory()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            updated_dict = None
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                session.commit()
                session.refresh(task)
                updated_dict = task.to_dict()
            return updated_dict
        finally:
            session.close()

    def delete_task(self, task_id: int):
        session = self.session_factory()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            deleted_task_dict = None
            if task:
                deleted_task_dict = task.to_dict()
                session.delete(task)
                session.commit()
                return deleted_task_dict
            return None
        finally:
            session.close()

    def clear_tasks(self):
        session = self.session_factory()
        try:
            session.query(Task).delete()
            session.commit()
            return True
        finally:
            session.close()
