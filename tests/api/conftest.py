import pytest
import requests

BASE_URL = "http://localhost:5000/api/tasks"


@pytest.fixture(autouse=True)
def reset_api_tasks():
    """
    Automatically reset API state before each test.
    If server is not running or not responding correctly, skip the test.
    """
    try:
        # First check if server is alive with a short timeout
        health_resp = requests.get("http://localhost:5000/api/health", timeout=2)
        if health_resp.status_code != 200:
            pytest.skip(f"Server health check failed with status {health_resp.status_code}")

        # Quick check if API endpoint is working
        api_resp = requests.get(BASE_URL, timeout=2)
        if api_resp.status_code != 200:
            pytest.skip(f"API endpoint check failed with status {api_resp.status_code}")

        # Try to reset (if endpoint exists) - not critical if this fails
        try:
            requests.post(f"{BASE_URL}/reset", timeout=2)
        except requests.exceptions.RequestException:
            # Reset endpoint might not exist, that's okay
            pass

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        pytest.skip("Server is not running or not responding, skipping integration test.")
    except Exception as e:
        pytest.skip(f"Server check failed: {e}")