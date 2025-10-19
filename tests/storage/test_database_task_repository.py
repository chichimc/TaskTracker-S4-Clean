import tempfile
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.sqlalchemy_task import Base
from app.repositories.database_task_repository import DatabaseTaskRepository


def test_add_and_get_tasks_in_memory(in_memory_repo):
    in_memory_repo.add_task("Test", "SQA Task")
    tasks = in_memory_repo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]['title'] == "Test"


def test_add_and_get_tasks_file_based():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        db_path = f"sqlite:///{tmp.name}"

    engine = None
    try:
        engine = create_engine(db_path)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        repo = DatabaseTaskRepository(Session)

        repo.add_task("File Test", "DB Test")
        tasks = repo.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['title'] == "File Test"
    finally:
        if engine:
            engine.dispose()

        import time
        time.sleep(0.1)

        try:
            os.remove(tmp.name)
        except PermissionError:
            pass


def test_add_and_get_tasks(session_factory):
    repo = DatabaseTaskRepository(session_factory)
    repo.add_task("Test", "SQA Task")
    tasks = repo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]['title'] == "Test"
