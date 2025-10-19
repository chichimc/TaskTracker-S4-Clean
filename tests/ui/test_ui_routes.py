# tests/ui/test_ui_routes.py
# ✅ TC-RF012-001: GET /tasks/new returns HTML form

def test_form_route_get(client):
    response = client.get("/tasks/new")
    assert response.status_code == 200
    assert b"<form" in response.data