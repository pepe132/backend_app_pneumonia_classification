from typing import Optional


FUSION_VERSION = "rules-v1.0"


def _recommendation_code(severity: str) -> str:
    return f"severity_{severity.strip().lower()}"


def fuse_results(
    tabular_severity: str,
    image_class: Optional[str] = None,
    image_confidence: Optional[float] = None,
    minimum_image_confidence: float = 0.60,
) -> dict:
    base_result = {
        "final_severity": tabular_severity,
        "recommendation_code": _recommendation_code(tabular_severity),
        "fusion_version": FUSION_VERSION,
    }

    if image_class is None:
        return {
            **base_result,
            "radiographic_support": "not_available",
            "concordance": "not_applicable",
            "basis": "tabular_only",
            "explanation": (
                "Severidad estimada únicamente con datos clínicos; "
                "no se incluyó una radiografía."
            ),
        }

    if image_confidence is None or image_confidence < minimum_image_confidence:
        return {
            **base_result,
            "radiographic_support": "indeterminate",
            "concordance": "indeterminate",
            "basis": "clinical_and_radiographic",
            "explanation": (
                "La radiografía fue analizada, pero la confianza del modelo de imagen "
                "es insuficiente. La severidad clínica no se modifica."
            ),
        }

    if image_class in {"pneumonia_bacterial", "pneumonia_viral"}:
        pneumonia_type = (
            "bacteriana" if image_class == "pneumonia_bacterial" else "viral"
        )
        return {
            **base_result,
            "radiographic_support": "supports_pneumonia",
            "concordance": "concordant",
            "basis": "clinical_and_radiographic",
            "explanation": (
                f"La radiografía aporta evidencia compatible con neumonía {pneumonia_type}. "
                "La severidad final permanece basada en los hallazgos clínicos."
            ),
        }

    if image_class == "normal":
        return {
            **base_result,
            "radiographic_support": "does_not_support_pneumonia",
            "concordance": "discordant",
            "basis": "clinical_and_radiographic",
            "explanation": (
                "El modelo clasificó la radiografía como normal. Esto no descarta el "
                "cuadro clínico ni reduce automáticamente la severidad estimada."
            ),
        }

    if image_class == "covid_19":
        return {
            **base_result,
            "radiographic_support": "review_required",
            "concordance": "indeterminate",
            "basis": "clinical_and_radiographic",
            "explanation": (
                "El modelo identificó un patrón compatible con COVID-19. Se requiere "
                "revisión clínica y confirmación mediante el protocolo institucional."
            ),
        }

    raise ValueError(f"Clase radiográfica no soportada: {image_class}")
