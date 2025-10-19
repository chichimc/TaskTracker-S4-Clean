# tests/api/conftest.py
import pytest
import requests

BASE_URL = "http://localhost:5000/api/tasks"

@pytest.fixture(autouse=True)
def reset_api_tasks():
    try:
        requests.post(f"{BASE_URL}/reset")
    except requests.exceptions.ConnectionError:
        pytest.skip("Server is not running, skipping integration test.")
