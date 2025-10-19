# tests/test_blueprint_routing.py
# All major routes work after blueprint modularization.
# None return 404.
# Functional responses are returned.
import pytest
from app import create_app



def test_routes_accessible_via_blueprint(client):
    """
    TC-NFR001-001: Ensure all routes are accessible after blueprint registration.
    """
    # Health check
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

    # Task list
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

    # Add task
    response = client.post("/api/tasks", json={
        "title": "Test Blueprint Route",
        "description": "Blueprint test"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == "Test Blueprint Route"