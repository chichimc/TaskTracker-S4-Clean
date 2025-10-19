# tests/test_health.py
from app import create_app

def test_health_check():
    """
    tc-us001-001: The /api/health endpoint should return a 200 OK with {"status": "ok"}.
    """
    app = create_app()
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}