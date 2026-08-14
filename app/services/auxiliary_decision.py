from typing import Any, Mapping


ClinicalPrediction = str
RadiographicPrediction = str

CLINICAL_CLASSES: tuple[str, ...] = ("Low", "Moderate", "High")
XRAY_CLASSES: tuple[str, ...] = (
    "COVID-19",
    "Normal",
    "Bacterial pneumonia",
    "Viral pneumonia",
)

PNEUMONIA_XRAY_CLASSES: set[str] = {
    "COVID-19",
    "Bacterial pneumonia",
    "Viral pneumonia",
}

URGENT_RECOMMENDATION = (
    "Se recomienda valoración médica urgente. Considerar referencia hospitalaria "
    "según criterio clínico."
)
SAFETY_NOTE = (
    "Este resultado es un apoyo auxiliar a la decisión clínica y no sustituye "
    "el juicio médico."
)


def _get_numeric_value(
    patient_data: Mapping[str, Any],
    field_name: str,
    *,
    required: bool = True,
) -> float | None:
    value = patient_data.get(field_name)
    if value is None:
        if required:
            raise ValueError(f"Falta el campo clínico requerido: {field_name}")
        return None

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"El campo clínico {field_name} debe ser numérico")

    return float(value)


def _get_binary_value(patient_data: Mapping[str, Any], field_name: str) -> int:
    value = patient_data.get(field_name)
    if value not in (0, 1, False, True):
        raise ValueError(f"El campo clínico {field_name} debe ser 0 o 1")
    return int(value)


def _get_optional_binary_value(patient_data: Mapping[str, Any], field_name: str) -> int:
    if field_name not in patient_data or patient_data.get(field_name) is None:
        return 0
    return _get_binary_value(patient_data, field_name)


def is_elevated_respiratory_rate(edad_meses: int, fr: float) -> bool:
    if edad_meses < 0:
        raise ValueError("edad_meses no puede ser negativo")

    if edad_meses < 2:
        return fr >= 60
    if edad_meses < 12:
        return fr >= 50
    if edad_meses < 60:
        return fr >= 40
    return fr >= 30


def identify_clinical_findings(patient_data: Mapping[str, Any]) -> list[str]:
    edad_meses = int(_get_numeric_value(patient_data, "edad_meses"))
    fr = _get_numeric_value(patient_data, "fr")
    spo2 = _get_numeric_value(patient_data, "spo2")
    temperatura_c = _get_numeric_value(patient_data, "temperatura_c")
    glasgow = _get_numeric_value(patient_data, "glasgow")
    dias_dificultad_respiratoria = _get_numeric_value(
        patient_data,
        "dias_dificultad_respiratoria",
    )

    findings: list[str] = []

    if spo2 < 92:
        findings.append("Baja saturación de oxígeno")
    if _get_binary_value(patient_data, "tiraje") == 1:
        findings.append("Presencia de tiraje")
    if _get_optional_binary_value(patient_data, "retraccion_xifoidea") == 1:
        findings.append("Retracción xifoidea")
    if _get_optional_binary_value(patient_data, "disociacion_toracoabdominal") == 1:
        findings.append("Disociación toracoabdominal")
    if is_elevated_respiratory_rate(edad_meses, fr):
        findings.append("Frecuencia respiratoria elevada")
    if temperatura_c >= 38:
        findings.append("Fiebre")
    if _get_binary_value(patient_data, "aleteo_nasal") == 1:
        findings.append("Aleteo nasal")
    if _get_binary_value(patient_data, "quejido_espiratorio") == 1:
        findings.append("Quejido espiratorio")
    if _get_binary_value(patient_data, "cianosis") == 1:
        findings.append("Cianosis")
    if _get_binary_value(patient_data, "apnea") == 1:
        findings.append("Apnea")
    if _get_binary_value(patient_data, "rechazo_comer") == 1:
        findings.append("Rechazo al alimento")
    if _get_optional_binary_value(patient_data, "vomita_todo") == 1:
        findings.append("Vómito persistente o imposibilidad para tolerar vía oral")
    if _get_binary_value(patient_data, "convulsiones") == 1:
        findings.append("Convulsiones")
    if glasgow < 15:
        findings.append("Puntaje de Glasgow disminuido")
    if _get_optional_binary_value(patient_data, "desnutricion") == 1:
        findings.append("Desnutrición")
    if _get_optional_binary_value(patient_data, "antecedentes_cronicos") == 1:
        findings.append("Antecedentes crónicos relevantes")
    if _get_optional_binary_value(patient_data, "sibilancias") == 1:
        findings.append("Sibilancias")
    if dias_dificultad_respiratoria >= 2:
        findings.append("Dificultad respiratoria persistente")
    if _get_optional_binary_value(patient_data, "crepitantes") == 1:
        findings.append("Crepitantes")
    if _get_optional_binary_value(patient_data, "disminucion_murmullo_vesicular") == 1:
        findings.append("Disminución del murmullo vesicular")
    if _get_optional_binary_value(patient_data, "dolor_toracico") == 1:
        findings.append("Dolor torácico")

    return findings


def has_warning_signs(patient_data: Mapping[str, Any]) -> bool:
    edad_meses = int(_get_numeric_value(patient_data, "edad_meses"))
    fr = _get_numeric_value(patient_data, "fr")
    spo2 = _get_numeric_value(patient_data, "spo2")
    glasgow = _get_numeric_value(patient_data, "glasgow")
    tiraje = _get_binary_value(patient_data, "tiraje")

    return any(
        (
            spo2 < 90,
            _get_binary_value(patient_data, "cianosis") == 1,
            _get_binary_value(patient_data, "apnea") == 1,
            _get_binary_value(patient_data, "convulsiones") == 1,
            glasgow < 14,
            is_elevated_respiratory_rate(edad_meses, fr) and tiraje == 1,
        )
    )


def validate_model_results(
    clinical_result: Mapping[str, Any],
    xray_result: Mapping[str, Any],
) -> None:
    _validate_single_model_result(
        result=clinical_result,
        expected_classes=CLINICAL_CLASSES,
        result_name="clinical_result",
    )
    _validate_single_model_result(
        result=xray_result,
        expected_classes=XRAY_CLASSES,
        result_name="xray_result",
    )


def _validate_single_model_result(
    *,
    result: Mapping[str, Any],
    expected_classes: tuple[str, ...],
    result_name: str,
) -> None:
    if not isinstance(result, Mapping):
        raise ValueError(f"{result_name} debe ser un objeto")

    prediction = result.get("prediction")
    if prediction not in expected_classes:
        expected = ", ".join(expected_classes)
        raise ValueError(
            f"{result_name}.prediction debe ser una de estas clases: {expected}"
        )

    probabilities = result.get("probabilities")
    if not isinstance(probabilities, Mapping):
        raise ValueError(f"{result_name}.probabilities debe ser un objeto")

    missing_classes = [
        class_name for class_name in expected_classes if class_name not in probabilities
    ]
    if missing_classes:
        missing = ", ".join(missing_classes)
        raise ValueError(
            f"Faltan probabilidades en {result_name}.probabilities: {missing}"
        )

    for class_name in expected_classes:
        probability = probabilities[class_name]
        if isinstance(probability, bool) or not isinstance(probability, (int, float)):
            raise ValueError(
                f"La probabilidad de {class_name} en {result_name} debe ser numérica"
            )
        if probability < 0 or probability > 1:
            raise ValueError(
                f"La probabilidad de {class_name} en {result_name} debe estar entre 0 y 1"
            )


def format_auxiliary_classification(clinical_result: Mapping[str, Any]) -> str:
    prediction = clinical_result["prediction"]
    probabilities = clinical_result["probabilities"]

    if prediction == "High":
        return (
            "Alta probabilidad de severidad alta "
            f"({float(probabilities['High']):.2%})."
        )
    if prediction == "Moderate":
        return (
            "Probabilidad moderada de severidad media "
            f"({float(probabilities['Moderate']):.2%})."
        )
    return (
        "Baja probabilidad de presentación clínica severa "
        f"({float(probabilities['Low']):.2%})."
    )


def format_radiographic_result(xray_result: Mapping[str, Any]) -> str:
    prediction = xray_result["prediction"]
    probabilities = xray_result["probabilities"]
    probability = float(probabilities[prediction])

    if prediction == "Normal":
        return (
            "El modelo no identificó un patrón radiográfico compatible con neumonía "
            f"({probability:.2%})."
        )
    if prediction == "Bacterial pneumonia":
        return (
            "Patrón radiográfico compatible con neumonía bacteriana "
            f"({probability:.2%})."
        )
    if prediction == "Viral pneumonia":
        return (
            "Patrón radiográfico compatible con neumonía viral "
            f"({probability:.2%})."
        )
    return f"Patrón radiográfico compatible con COVID-19 ({probability:.2%})."


def generate_recommendation(
    clinical_prediction: ClinicalPrediction,
    xray_prediction: RadiographicPrediction,
    warning_signs: bool,
) -> str:
    if clinical_prediction == "High" or warning_signs:
        return URGENT_RECOMMENDATION

    if clinical_prediction == "Moderate":
        if xray_prediction in PNEUMONIA_XRAY_CLASSES:
            return (
                "Se recomienda valoración médica y vigilancia estrecha. Los hallazgos "
                "radiográficos deben correlacionarse con los signos clínicos."
            )
        return (
            "Se recomienda vigilancia clínica. Se aconseja reevaluación si los síntomas "
            "empeoran o aparecen signos de alarma."
        )

    if xray_prediction in PNEUMONIA_XRAY_CLASSES:
        return (
            "Se estimó baja severidad clínica, pero el modelo radiográfico sugiere un "
            "patrón compatible con neumonía. Se recomienda correlación médica."
        )

    return (
        "Se estimó baja severidad clínica. Se recomienda seguimiento y educación "
        "sobre signos de alarma."
    )


def generate_auxiliary_decision(
    clinical_result: Mapping[str, Any],
    xray_result: Mapping[str, Any],
    patient_data: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(patient_data, Mapping):
        raise ValueError("patient_data debe ser un objeto")

    validate_model_results(clinical_result, xray_result)

    findings = identify_clinical_findings(patient_data)
    warning_signs = has_warning_signs(patient_data)

    return {
        "clasificacion_auxiliar": format_auxiliary_classification(clinical_result),
        "prediccion_severidad": clinical_result["prediction"],
        "probabilidades_severidad": dict(clinical_result["probabilities"]),
        "hallazgos_clinicos_relevantes": findings,
        "resultado_radiografico_auxiliar": format_radiographic_result(xray_result),
        "prediccion_radiografica": xray_result["prediction"],
        "probabilidades_radiograficas": dict(xray_result["probabilities"]),
        "recomendacion": generate_recommendation(
            clinical_prediction=clinical_result["prediction"],
            xray_prediction=xray_result["prediction"],
            warning_signs=warning_signs,
        ),
        "nota_seguridad": SAFETY_NOTE,
    }
