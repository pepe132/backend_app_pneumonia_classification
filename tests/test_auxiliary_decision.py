import pytest

from app.services.auxiliary_decision import (
    generate_auxiliary_decision,
    is_elevated_respiratory_rate,
)


@pytest.mark.parametrize(
    ("age_months", "rate", "expected"),
    [(1, 60, True), (2, 50, True), (11, 49, False), (12, 40, True), (59, 39, False), (60, 30, True), (72, 29, False)],
)
def test_respiratory_rate_thresholds(age_months, rate, expected):
    assert is_elevated_respiratory_rate(age_months, rate) is expected


def test_low_severity_without_alarms_returns_followup(
    low_clinical_result,
    normal_xray_result,
    patient_data,
):
    result = generate_auxiliary_decision(
        low_clinical_result,
        normal_xray_result,
        patient_data,
    )

    assert result["prediccion_severidad"] == "Low"
    assert result["prediccion_radiografica"] == "Normal"
    assert result["hallazgos_clinicos_relevantes"] == []
    assert "seguimiento" in result["recomendacion"].lower()
    assert "no sustituye" in result["nota_seguridad"].lower()


@pytest.mark.parametrize(
    ("field", "value"),
    [("spo2", 89), ("cianosis", True), ("apnea", True), ("convulsiones", True), ("glasgow", 13)],
)
def test_warning_signs_raise_urgent_recommendation(
    field,
    value,
    low_clinical_result,
    normal_xray_result,
    patient_data,
):
    patient_data[field] = value

    result = generate_auxiliary_decision(
        low_clinical_result,
        normal_xray_result,
        patient_data,
    )

    assert "urgente" in result["recomendacion"].lower()


def test_fast_breathing_with_retractions_is_urgent(
    low_clinical_result,
    normal_xray_result,
    patient_data,
):
    patient_data.update({"fr": 50, "tiraje": True})

    result = generate_auxiliary_decision(
        low_clinical_result,
        normal_xray_result,
        patient_data,
    )

    assert "Frecuencia respiratoria elevada" in result["hallazgos_clinicos_relevantes"]
    assert "Presencia de tiraje" in result["hallazgos_clinicos_relevantes"]
    assert "urgente" in result["recomendacion"].lower()


def test_missing_model_probability_is_rejected(
    low_clinical_result,
    normal_xray_result,
    patient_data,
):
    del low_clinical_result["probabilities"]["High"]

    with pytest.raises(ValueError, match="Faltan probabilidades"):
        generate_auxiliary_decision(
            low_clinical_result,
            normal_xray_result,
            patient_data,
        )
