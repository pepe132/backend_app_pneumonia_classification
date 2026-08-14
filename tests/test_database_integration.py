import uuid

import pytest

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

    search = db_client.get(
        "/patients/search", params={"q": name}, headers=reader_headers
    )
    assert search.status_code == 200
    assert patient_id in {patient["patient_id"] for patient in search.json()}

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
