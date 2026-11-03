import pytest

from app.services.auxiliary_decision import (
    generate_auxiliary_decision,
    generate_clinical_only_decision,
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


def test_low_confidence_xray_does_not_influence_recommendation(
    low_clinical_result,
    normal_xray_result,
    patient_data,
):
    normal_xray_result["prediction"] = "Viral pneumonia"
    normal_xray_result["probabilities"] = {
        "COVID-19": 0.10,
        "Normal": 0.20,
        "Bacterial pneumonia": 0.25,
        "Viral pneumonia": 0.45,
    }

    result = generate_auxiliary_decision(
        low_clinical_result,
        normal_xray_result,
        patient_data,
        radiographic_evidence_reliable=False,
    )

    assert "confianza fue insuficiente" in result["resultado_radiografico_auxiliar"]
    assert "seguimiento" in result["recomendacion"].lower()
    assert "correlación médica" not in result["recomendacion"].lower()


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


def test_clinical_only_decision_has_fusion_metadata(
    low_clinical_result,
    patient_data,
):
    result = generate_clinical_only_decision(low_clinical_result, patient_data)

    assert result["prediccion_radiografica"] is None
    assert result["fusion_method"] == "rules"
    assert result["nivel_atencion"] == "CARE-FOLLOWUP"
    assert result["reglas_activadas"] == []


def test_warning_rule_is_traceable(
    low_clinical_result,
    patient_data,
):
    patient_data.update({"spo2": 88, "tiraje": True, "fr": 50})

    result = generate_clinical_only_decision(low_clinical_result, patient_data)

    assert "ALARM-001" in result["reglas_activadas"]
    assert "RESP-001" in result["reglas_activadas"]
    assert result["nivel_atencion"] == "CARE-URGENT"
