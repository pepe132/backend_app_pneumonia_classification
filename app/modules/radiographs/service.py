import json
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.config import CNN_MIN_CONFIDENCE, RADIOGRAPH_MAX_SIZE_MB
from app.modules.evaluations.fusion import fuse_results
from app.modules.evaluations.models import Evaluation
from app.modules.radiographs.models import Radiograph
from app.modules.radiographs.predictor import predict_radiograph
from app.modules.radiographs.storage import delete_radiograph, save_radiograph
from app.services.auxiliary_decision import generate_auxiliary_decision


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
SEVERITY_LABELS = {
    "bajo": "Low",
    "low": "Low",
    "medio": "Moderate",
    "moderate": "Moderate",
    "medium": "Moderate",
    "alto": "High",
    "high": "High",
}
XRAY_LABELS = {
    "covid_19": "COVID-19",
    "normal": "Normal",
    "pneumonia_bacterial": "Bacterial pneumonia",
    "pneumonia_viral": "Viral pneumonia",
}


class RadiographAlreadyExistsError(ValueError):
    pass


class InvalidRadiographError(ValueError):
    pass


def get_radiograph_by_evaluation(
    db: Session,
    evaluation_id: str,
) -> Optional[Radiograph]:
    return (
        db.query(Radiograph)
        .filter(Radiograph.evaluation_id == evaluation_id)
        .first()
    )


async def analyze_radiograph(
    db: Session,
    evaluation: Evaluation,
    upload: UploadFile,
    user_id: str,
) -> dict:
    if get_radiograph_by_evaluation(db, evaluation.evaluation_id):
        raise RadiographAlreadyExistsError(
            "La evaluación ya tiene una radiografía analizada."
        )
    if not evaluation.severity_tabular:
        raise InvalidRadiographError(
            "La evaluación no contiene una predicción tabular válida."
        )

    content_type = (upload.content_type or "").lower()
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise InvalidRadiographError("Solo se permiten imágenes JPG o PNG.")

    max_size = RADIOGRAPH_MAX_SIZE_MB * 1024 * 1024
    image_bytes = await upload.read(max_size + 1)
    if not image_bytes:
        raise InvalidRadiographError("La radiografía está vacía.")
    if len(image_bytes) > max_size:
        raise InvalidRadiographError(
            f"La radiografía supera el límite de {RADIOGRAPH_MAX_SIZE_MB} MB."
        )

    prediction = await run_in_threadpool(predict_radiograph, image_bytes)
    integrated_result = fuse_results(
        tabular_severity=evaluation.severity_tabular,
        image_class=prediction["image_class"],
        image_confidence=prediction["confidence"],
        minimum_image_confidence=CNN_MIN_CONFIDENCE,
    )

    file_path = save_radiograph(image_bytes, content_type)
    radiograph = Radiograph(
        radiograph_id=str(uuid.uuid4()),
        evaluation_id=evaluation.evaluation_id,
        uploaded_by=user_id,
        file_path=file_path,
        original_filename=Path(upload.filename or "radiograph").name,
        content_type=content_type,
        file_size=len(image_bytes),
        image_class=prediction["image_class"],
        confidence=prediction["confidence"],
        prob_covid=prediction["prob_covid"],
        prob_normal=prediction["prob_normal"],
        prob_bacterial=prediction["prob_bacterial"],
        prob_viral=prediction["prob_viral"],
        model_version=prediction["model_version"],
    )

    evaluation.final_severity = integrated_result["final_severity"]
    evaluation.radiographic_support = integrated_result["radiographic_support"]
    evaluation.concordance = integrated_result["concordance"]
    evaluation.fusion_basis = integrated_result["basis"]
    evaluation.fusion_explanation = integrated_result["explanation"]
    evaluation.recommendation_code = integrated_result["recommendation_code"]
    evaluation.fusion_version = integrated_result["fusion_version"]
    auxiliary_decision = build_auxiliary_decision(evaluation, radiograph)
    evaluation.auxiliary_decision_json = json.dumps(
        auxiliary_decision, ensure_ascii=False
    )

    try:
        db.add(radiograph)
        db.commit()
        db.refresh(radiograph)
        db.refresh(evaluation)
    except Exception:
        db.rollback()
        delete_radiograph(file_path)
        raise

    return {
        "radiograph": serialize_radiograph(radiograph),
        "integrated_result": integrated_result,
        "auxiliary_decision": auxiliary_decision,
    }


def serialize_radiograph(radiograph: Radiograph) -> dict:
    return {
        "radiograph_id": radiograph.radiograph_id,
        "evaluation_id": radiograph.evaluation_id,
        "uploaded_by": radiograph.uploaded_by,
        "original_filename": radiograph.original_filename,
        "content_type": radiograph.content_type,
        "file_size": radiograph.file_size,
        "image_class": radiograph.image_class,
        "confidence": radiograph.confidence,
        "probabilities": {
            "covid_19": radiograph.prob_covid,
            "normal": radiograph.prob_normal,
            "pneumonia_bacterial": radiograph.prob_bacterial,
            "pneumonia_viral": radiograph.prob_viral,
        },
        "pneumonia_probability": round(
            radiograph.prob_bacterial + radiograph.prob_viral,
            6,
        ),
        "model_version": radiograph.model_version,
        "created_at": radiograph.created_at,
    }


def build_auxiliary_decision(
    evaluation: Evaluation,
    radiograph: Radiograph,
) -> dict:
    clinical_result = {
        "prediction": _normalize_severity_label(evaluation.severity_tabular),
        "probabilities": {
            "Low": evaluation.prob_low,
            "Moderate": evaluation.prob_medium,
            "High": evaluation.prob_high,
        },
    }
    xray_result = {
        "prediction": _normalize_xray_label(radiograph.image_class),
        "probabilities": {
            "COVID-19": radiograph.prob_covid,
            "Normal": radiograph.prob_normal,
            "Bacterial pneumonia": radiograph.prob_bacterial,
            "Viral pneumonia": radiograph.prob_viral,
        },
    }

    return generate_auxiliary_decision(
        clinical_result=clinical_result,
        xray_result=xray_result,
        patient_data=_evaluation_to_patient_data(evaluation),
    )


def _normalize_severity_label(severity: str | None) -> str:
    if not severity:
        raise ValueError("La evaluación no contiene severidad clínica")

    normalized = SEVERITY_LABELS.get(severity.strip().lower())
    if not normalized:
        raise ValueError(f"Severidad clínica no soportada: {severity}")
    return normalized


def _normalize_xray_label(image_class: str) -> str:
    normalized = XRAY_LABELS.get(image_class)
    if not normalized:
        raise ValueError(f"Clase radiográfica no soportada: {image_class}")
    return normalized


def _evaluation_to_patient_data(evaluation: Evaluation) -> dict:
    return {
        "patient_id": evaluation.patient_id,
        "edad_meses": evaluation.edad_meses,
        "peso_kg": evaluation.peso_kg,
        "spo2": evaluation.spo2,
        "fr": evaluation.fr,
        "fc": evaluation.fc,
        "temperatura_c": evaluation.temperatura_c,
        "tiraje": evaluation.tiraje,
        "retraccion_xifoidea": evaluation.retraccion_xifoidea,
        "disociacion_toracoabdominal": evaluation.disociacion_toracoabdominal,
        "aleteo_nasal": evaluation.aleteo_nasal,
        "quejido_espiratorio": evaluation.quejido_espiratorio,
        "cianosis": evaluation.cianosis,
        "apnea": evaluation.apnea,
        "rechazo_comer": evaluation.rechazo_comer,
        "vomita_todo": evaluation.vomita_todo,
        "convulsiones": evaluation.convulsiones,
        "glasgow": evaluation.glasgow,
        "desnutricion": evaluation.desnutricion,
        "antecedentes_cronicos": evaluation.antecedentes_cronicos,
        "sibilancias": evaluation.sibilancias,
        "dias_sintomas": evaluation.dias_sintomas,
        "dias_fiebre": evaluation.dias_fiebre,
        "dias_tos": evaluation.dias_tos,
        "dias_dificultad_respiratoria": evaluation.dias_dificultad_respiratoria,
        "crepitantes": evaluation.crepitantes,
        "disminucion_murmullo_vesicular": evaluation.disminucion_murmullo_vesicular,
        "dolor_toracico": evaluation.dolor_toracico,
    }
