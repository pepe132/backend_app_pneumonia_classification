import pytest
from pydantic import ValidationError

from app.modules.auth.schema import RegisterRequest
from app.modules.decision.schema import PatientData
from app.modules.evaluations.schema import EvaluationCreate
from app.modules.patients.schema import PatientCreate


def test_user_name_limit_matches_database():
    valid = RegisterRequest(
        user_name="A" * 40,
        email="valid@example.com",
        role_id=2,
        user_password="password123",
    )
    assert len(valid.user_name) == 40

    with pytest.raises(ValidationError):
        RegisterRequest(
            user_name="A" * 41,
            email="invalid@example.com",
            role_id=2,
            user_password="password123",
        )


def test_email_limit_matches_database():
    local_part = "a" * 38
    valid = RegisterRequest(
        user_name="Test",
        email=f"{local_part}@example.com",
        role_id=2,
        user_password="password123",
    )
    assert len(valid.email) == 50

    with pytest.raises(ValidationError):
        RegisterRequest(
            user_name="Test",
            email=f"{local_part}b@example.com",
            role_id=2,
            user_password="password123",
        )


@pytest.mark.parametrize("age_months", [0, 1, 2, 59, 60, 72])
def test_patient_accepts_supported_age_range(age_months):
    patient = PatientCreate(full_name="Test", age_months=age_months, sex="M")
    assert patient.age_months == age_months


@pytest.mark.parametrize("age_months", [-1, 73])
def test_patient_rejects_unsupported_age(age_months):
    with pytest.raises(ValidationError):
        PatientCreate(full_name="Test", age_months=age_months, sex="F")


@pytest.mark.parametrize(
    "overrides",
    [{"weight": 0}, {"weight": 151}, {"height": 0}, {"height": 251}, {"sex": "X"}],
)
def test_patient_rejects_invalid_demographic_values(overrides):
    payload = {"full_name": "Test", "age_months": 36, "sex": "M", **overrides}
    with pytest.raises(ValidationError):
        PatientCreate(**payload)


def _evaluation_payload(age_months):
    return {
        "patient_id": "test-patient",
        "edad_meses": age_months,
        "peso_kg": 14,
        "fr": 40,
        "fc": 120,
        "temperatura_c": 37,
        "spo2": 95,
        "glasgow": 15,
        "dias_sintomas": 1,
        "dias_fiebre": 0,
        "dias_tos": 1,
        "dias_dificultad_respiratoria": 0,
    }


def test_age_limit_is_consistent_across_clinical_schemas():
    assert EvaluationCreate(**_evaluation_payload(72)).edad_meses == 72
    decision_payload = {
        key: value
        for key, value in _evaluation_payload(72).items()
        if key != "patient_id" and key != "peso_kg"
    }
    assert PatientData(**decision_payload).edad_meses == 72

    with pytest.raises(ValidationError):
        EvaluationCreate(**_evaluation_payload(73))
    with pytest.raises(ValidationError):
        PatientData(**{**decision_payload, "edad_meses": 73})
