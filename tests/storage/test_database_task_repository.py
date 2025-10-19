# tests/storage/test_database_task_repository.py

import tempfile
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.sqlalchemy_task import Base
from app.repositories.database_task_repository import DatabaseTaskRepository


# ✅ TC-RF010-001: Add and Retrieve Tasks from DB (in-memory SQLite)

def test_add_and_get_tasks_in_memory(in_memory_repo):
    in_memory_repo.add_task("Test", "SQA Task")
    tasks = in_memory_repo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test"


# ✅ TC-RF010-002: Add and Retrieve Tasks from DB (test file SQLite)

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
        assert tasks[0].title == "File Test"
    finally:
        # Properly close all connections before deleting the file
        if engine:
            engine.dispose()

        # Give Windows a moment to release the file handles
        import time
        time.sleep(0.1)

        try:
            os.remove(tmp.name)
        except PermissionError:
            # If still can't delete, it's not a critical failure for the test
            pass


# ✅ TC-RF010-003: Add and Retrieve Tasks from DB (Flask app-injected session)

def test_add_and_get_tasks(session_factory):
    repo = DatabaseTaskRepository(session_factory)
    repo.add_task("Test", "SQA Task")
    tasks = repo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test"

# ⚠️ Note: This test will raise NameError until session_factory is configured via the Flask app. You’ll revisit this in later phases.