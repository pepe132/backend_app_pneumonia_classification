import uuid

import pytest

from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.radiographs import service as radiograph_service
from app.modules.radiographs import storage as radiograph_storage


pytestmark = pytest.mark.database

TEST_PASSWORD = "PruebaSegura_2026!"


def unique_email(prefix):
    return f"{prefix[:10]}.{uuid.uuid4().hex[:12]}@example.com"


def register_and_login(client, role_id, prefix):
    email = unique_email(prefix)
    register = client.post(
        "/auth/register",
        json={
            "user_name": f"QA_{prefix}_{uuid.uuid4().hex[:8]}",
            "email": email,
            "role_id": role_id,
            "user_password": TEST_PASSWORD,
        },
    )
    assert register.status_code == 200

    login = client.post(
        "/auth/login",
        json={"email": email, "user_password": TEST_PASSWORD},
    )
    assert login.status_code == 200
    return register.json(), {
        "Authorization": f"Bearer {login.json()['access_token']}"
    }


def create_admin_and_login(client, db_session):
    email = unique_email("admin")
    admin = User(
        user_id=str(uuid.uuid4()),
        user_name="QA_ADMIN",
        email=email,
        role_id=1,
        active=True,
        user_password=hash_password(TEST_PASSWORD),
    )
    db_session.add(admin)
    db_session.commit()
    login = client.post(
        "/auth/login",
        json={"email": email, "user_password": TEST_PASSWORD},
    )
    assert login.status_code == 200
    return admin, {"Authorization": f"Bearer {login.json()['access_token']}"}


def patient_payload(name=None):
    return {
        "full_name": name or f"QA_PATIENT_{uuid.uuid4().hex}",
        "age_months": 36,
        "sex": "M",
        "weight": 14.0,
        "height": 95.0,
        "guardian_name": "QA_GUARDIAN",
    }


def evaluation_payload(patient_id):
    return {
        "patient_id": patient_id,
        "edad_meses": 36,
        "peso_kg": 14.0,
        "fr": 50,
        "fc": 135,
        "temperatura_c": 38.2,
        "spo2": 91,
        "tiraje": True,
        "retraccion_xifoidea": True,
        "disociacion_toracoabdominal": False,
        "aleteo_nasal": True,
        "quejido_espiratorio": False,
        "cianosis": False,
        "apnea": False,
        "rechazo_comer": True,
        "vomita_todo": False,
        "convulsiones": False,
        "glasgow": 15,
        "desnutricion": False,
        "antecedentes_cronicos": False,
        "sibilancias": True,
        "dias_sintomas": 5,
        "dias_fiebre": 3,
        "dias_tos": 5,
        "dias_dificultad_respiratoria": 5,
        "crepitantes": True,
        "disminucion_murmullo_vesicular": False,
        "dolor_toracico": False,
    }


def test_authentication_workflow_persists_inside_transaction(db_client):
    email = unique_email("auth")
    payload = {
        "user_name": "QA_AUTH_USER",
        "email": email,
        "role_id": 2,
        "user_password": TEST_PASSWORD,
    }

    register = db_client.post("/auth/register", json=payload)
    assert register.status_code == 200
    assert "user_password" not in register.json()

    duplicate = db_client.post("/auth/register", json=payload)
    assert duplicate.status_code == 400

    forbidden_admin = db_client.post(
        "/auth/register",
        json={**payload, "email": unique_email("admin"), "role_id": 1},
    )
    assert forbidden_admin.status_code == 403

    invalid_login = db_client.post(
        "/auth/login",
        json={"email": email, "user_password": "Incorrecta_2026!"},
    )
    assert invalid_login.status_code == 401

    login = db_client.post(
        "/auth/login",
        json={"email": email, "user_password": TEST_PASSWORD},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = db_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == email

    versioned_me = db_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert versioned_me.status_code == 200
    assert versioned_me.json()["user_id"] == me.json()["user_id"]


def test_auxiliary_decision_requires_clinical_write_role(
    db_client, low_clinical_result, normal_xray_result, patient_data
):
    _, specialist_headers = register_and_login(
        db_client, 2, "decision-specialist"
    )
    _, reader_headers = register_and_login(db_client, 3, "decision-reader")
    payload = {
        "clinical_result": low_clinical_result,
        "xray_result": normal_xray_result,
        "patient_data": patient_data,
    }

    forbidden = db_client.post(
        "/decision/auxiliary", json=payload, headers=reader_headers
    )
    assert forbidden.status_code == 403

    allowed = db_client.post(
        "/decision/auxiliary", json=payload, headers=specialist_headers
    )
    assert allowed.status_code == 200
    assert allowed.json()["prediccion_severidad"] == "Low"


def test_admin_user_management_and_password_flows(db_client, db_session):
    admin, admin_headers = create_admin_and_login(db_client, db_session)
    _, specialist_headers = register_and_login(db_client, 2, "managed-specialist")

    assert db_client.get("/auth/users", headers=specialist_headers).status_code == 403

    email = unique_email("managed")
    created = db_client.post(
        "/auth/users",
        headers=admin_headers,
        json={
            "user_name": "QA_MANAGED_USER",
            "email": email,
            "role_id": 3,
            "user_password": TEST_PASSWORD,
        },
    )
    assert created.status_code == 201
    user_id = created.json()["user_id"]

    updated = db_client.patch(
        f"/auth/users/{user_id}",
        headers=admin_headers,
        json={"role_id": 2},
    )
    assert updated.status_code == 200
    assert updated.json()["role_id"] == 2

    new_password = "NuevaSegura_2026!"
    reset = db_client.post(
        f"/auth/users/{user_id}/reset-password",
        headers=admin_headers,
        json={"new_password": new_password},
    )
    assert reset.status_code == 204
    login = db_client.post(
        "/auth/login", json={"email": email, "user_password": new_password}
    )
    assert login.status_code == 200
    user_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    changed_password = "OtraSegura_2026!"
    changed = db_client.post(
        "/auth/change-password",
        headers=user_headers,
        json={
            "current_password": new_password,
            "new_password": changed_password,
        },
    )
    assert changed.status_code == 204

    assert db_client.delete(
        f"/auth/users/{admin.user_id}", headers=admin_headers
    ).status_code == 409
    assert db_client.delete(
        f"/auth/users/{user_id}", headers=admin_headers
    ).status_code == 204
    assert db_client.get("/auth/me", headers=user_headers).status_code == 401


def test_patient_crud_search_and_soft_delete(db_client):
    specialist, specialist_headers = register_and_login(
        db_client, 2, "patient-specialist"
    )
    _, reader_headers = register_and_login(db_client, 3, "patient-reader")
    name = f"QA_SEARCH_{uuid.uuid4().hex}"

    reader_create = db_client.post(
        "/patients/", json=patient_payload(name), headers=reader_headers
    )
    assert reader_create.status_code == 403

    create = db_client.post(
        "/patients/", json=patient_payload(name), headers=specialist_headers
    )
    assert create.status_code == 201
    patient_id = create.json()["patient_id"]
    assert create.json()["created_by"] == specialist["user_id"]

    get_patient = db_client.get(f"/patients/{patient_id}", headers=reader_headers)
    assert get_patient.status_code == 200
    assert get_patient.json()["created_by"] == specialist["user_id"]
    versioned_get = db_client.get(
        f"/api/v1/patients/{patient_id}", headers=reader_headers
    )
    assert versioned_get.status_code == 200

    search = db_client.get(
        "/patients/search", params={"q": name}, headers=reader_headers
    )
    assert search.status_code == 200
    assert patient_id in {patient["patient_id"] for patient in search.json()}

    page = db_client.get(
        "/patients/page",
        params={"search": name, "sex": "M", "page_size": 1},
        headers=reader_headers,
    )
    assert page.status_code == 200
    assert page.json()["total"] == 1
    assert page.json()["items"][0]["patient_id"] == patient_id

    reader_update = db_client.patch(
        f"/patients/{patient_id}", json={"weight": 99}, headers=reader_headers
    )
    assert reader_update.status_code == 403

    update = db_client.patch(
        f"/patients/{patient_id}", json={"weight": 15}, headers=specialist_headers
    )
    assert update.status_code == 200
    assert update.json()["weight"] == 15

    delete = db_client.delete(
        f"/patients/{patient_id}", headers=specialist_headers
    )
    assert delete.status_code == 204
    assert db_client.get(f"/patients/{patient_id}", headers=reader_headers).status_code == 404


def test_evaluation_runs_model_and_persists_prediction(db_client):
    specialist, specialist_headers = register_and_login(
        db_client, 2, "evaluation-specialist"
    )
    _, reader_headers = register_and_login(db_client, 3, "evaluation-reader")
    patient = db_client.post(
        "/patients/", json=patient_payload(), headers=specialist_headers
    ).json()
    payload = evaluation_payload(patient["patient_id"])

    forbidden = db_client.post("/evaluations", json=payload, headers=reader_headers)
    assert forbidden.status_code == 403

    create = db_client.post("/evaluations", json=payload, headers=specialist_headers)
    assert create.status_code == 201
    body = create.json()
    assert body["created_by"] == specialist["user_id"]
    assert body["severity_tabular"] in {"Bajo", "Medio", "Alto"}
    probabilities = [body["prob_low"], body["prob_medium"], body["prob_high"]]
    assert all(0 <= probability <= 1 for probability in probabilities)
    assert sum(probabilities) == pytest.approx(1.0, abs=0.001)

    evaluation_id = body["evaluation_id"]
    get_evaluation = db_client.get(
        f"/evaluations/{evaluation_id}", headers=reader_headers
    )
    assert get_evaluation.status_code == 200
    assert get_evaluation.json()["severity_tabular"] == body["severity_tabular"]

    history = db_client.get(
        f"/patients/{patient['patient_id']}/evaluations", headers=reader_headers
    )
    assert history.status_code == 200
    assert evaluation_id in {
        evaluation["evaluation_id"] for evaluation in history.json()
    }

    page = db_client.get(
        "/evaluations/page",
        params={"patient_id": patient["patient_id"], "page_size": 1},
        headers=reader_headers,
    )
    assert page.status_code == 200
    assert page.json()["total"] == 1
    assert page.json()["items"][0]["evaluation_id"] == evaluation_id

    report = db_client.get(
        f"/reports/evaluations/{evaluation_id}", headers=reader_headers
    )
    assert report.status_code == 200
    assert report.json()["patient"]["patient_id"] == patient["patient_id"]
    assert report.json()["radiograph"] is None

    dashboard = db_client.get("/dashboard/summary", headers=reader_headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["evaluations"] >= 1
    assert any(
        item["label"] == body["severity_tabular"]
        for item in dashboard.json()["severity_tabular"]
    )


def test_radiograph_upload_uses_mocked_predictor_and_persists(
    db_client,
    monkeypatch,
    tmp_path,
):
    _, specialist_headers = register_and_login(
        db_client, 2, "radiograph-specialist"
    )
    _, reader_headers = register_and_login(db_client, 3, "radiograph-reader")
    patient = db_client.post(
        "/patients/", json=patient_payload(), headers=specialist_headers
    ).json()
    evaluation = db_client.post(
        "/evaluations",
        json=evaluation_payload(patient["patient_id"]),
        headers=specialist_headers,
    ).json()

    monkeypatch.setattr(radiograph_storage, "RADIOGRAPH_UPLOAD_DIR", str(tmp_path))
    monkeypatch.setattr(
        radiograph_service,
        "predict_radiograph",
        lambda _: {
            "image_class": "pneumonia_viral",
            "confidence": 0.85,
            "prob_covid": 0.02,
            "prob_normal": 0.03,
            "prob_bacterial": 0.10,
            "prob_viral": 0.85,
            "pneumonia_probability": 0.95,
            "model_version": "mock-cnn-v1",
        },
    )

    evaluation_id = evaluation["evaluation_id"]
    reader_upload = db_client.post(
        f"/evaluations/{evaluation_id}/radiograph",
        headers=reader_headers,
        files={"file": ("test.jpg", b"fake-image", "image/jpeg")},
    )
    assert reader_upload.status_code == 403

    upload = db_client.post(
        f"/evaluations/{evaluation_id}/radiograph",
        headers=specialist_headers,
        files={"file": ("test.jpg", b"fake-image", "image/jpeg")},
    )
    assert upload.status_code == 201
    body = upload.json()
    assert body["radiograph"]["image_class"] == "pneumonia_viral"
    assert body["integrated_result"]["final_severity"] == evaluation["severity_tabular"]
    assert body["auxiliary_decision"]["prediccion_radiografica"] == "Viral pneumonia"

    duplicate = db_client.post(
        f"/evaluations/{evaluation_id}/radiograph",
        headers=specialist_headers,
        files={"file": ("test.jpg", b"fake-image", "image/jpeg")},
    )
    assert duplicate.status_code == 409

    get_radiograph = db_client.get(
        f"/evaluations/{evaluation_id}/radiograph", headers=reader_headers
    )
    assert get_radiograph.status_code == 200
    assert get_radiograph.json()["model_version"] == "mock-cnn-v1"

    image = db_client.get(
        f"/evaluations/{evaluation_id}/radiograph/image", headers=reader_headers
    )
    assert image.status_code == 200
    assert image.content == b"fake-image"
    assert image.headers["content-type"] == "image/jpeg"

    decision = db_client.get(
        f"/evaluations/{evaluation_id}/auxiliary-decision",
        headers=reader_headers,
    )
    assert decision.status_code == 200
    assert decision.json() == body["auxiliary_decision"]

    report = db_client.get(
        f"/reports/evaluations/{evaluation_id}", headers=reader_headers
    )
    assert report.status_code == 200
    assert report.json()["radiograph"]["image_class"] == "pneumonia_viral"
    assert report.json()["auxiliary_decision"] == body["auxiliary_decision"]

    filtered = db_client.get(
        "/evaluations/page",
        params={"patient_id": patient["patient_id"], "has_radiograph": True},
        headers=reader_headers,
    )
    assert filtered.status_code == 200
    assert filtered.json()["total"] == 1
