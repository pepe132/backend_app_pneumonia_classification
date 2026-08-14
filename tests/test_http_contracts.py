from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_and_openapi_are_available():
    assert client.get("/").status_code == 200
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    assert "/evaluations" in openapi.json()["paths"]


def test_protected_resources_reject_missing_token():
    assert client.get("/auth/me").status_code == 401
    assert client.get("/patients/").status_code == 401
    assert client.get("/evaluations").status_code == 401


def test_auxiliary_decision_rejects_incomplete_payload():
    response = client.post("/decision/auxiliary", json={})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    missing_fields = {detail["field"] for detail in error["details"]}
    assert missing_fields == {
        "body.clinical_result",
        "body.xray_result",
        "body.patient_data",
    }
    assert all("input" not in detail for detail in error["details"])
