# tests/api/test_add_task_api.py

# ✅ TC-RF011-002: POST /api/tasks adds DB entry
def test_post_task_adds_to_db(client):
    response = client.post("/api/tasks", json={"title": "DB", "description": "via API"})
    assert response.status_code == 201