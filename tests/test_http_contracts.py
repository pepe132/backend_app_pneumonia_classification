from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


client = TestClient(app)


def test_root_and_openapi_are_available():
    assert client.get("/").status_code == 200
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    assert "/evaluations" in openapi.json()["paths"]
    assert "/api/v1/evaluations" in openapi.json()["paths"]
    assert "/api/v1/patients/page" in openapi.json()["paths"]
    assert "/api/v1/reports/evaluations/{evaluation_id}" in openapi.json()["paths"]


def test_protected_resources_reject_missing_token():
    assert client.get("/auth/me").status_code == 401
    assert client.get("/patients/").status_code == 401
    assert client.get("/evaluations").status_code == 401
    assert client.post("/decision/auxiliary", json={}).status_code == 401
    assert client.get("/auth/users").status_code == 401
    assert client.post("/auth/change-password", json={}).status_code == 401
    assert client.get("/evaluations/test/radiograph/image").status_code == 401
    assert client.get("/evaluations/test/auxiliary-decision").status_code == 401
    assert client.get("/patients/page").status_code == 401
    assert client.get("/evaluations/page").status_code == 401
    assert client.get("/reports/evaluations/test").status_code == 401
    assert client.get("/dashboard/summary").status_code == 401
    assert client.get("/api/v1/patients/").status_code == 401
    assert client.get("/api/v1/evaluations").status_code == 401


def test_public_registration_can_be_disabled(monkeypatch):
    monkeypatch.setattr(settings, "allow_public_registration", False)
    response = client.post(
        "/auth/register",
        json={
            "user_name": "Blocked registration",
            "email": "blocked@example.com",
            "role_id": 2,
            "user_password": "Password_2026!",
        },
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
