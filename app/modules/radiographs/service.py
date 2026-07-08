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


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}


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

    try:
        db.add(radiograph)
        db.commit()
        db.refresh(radiograph)
    except Exception:
        db.rollback()
        delete_radiograph(file_path)
        raise

    return {
        "radiograph": serialize_radiograph(radiograph),
        "integrated_result": integrated_result,
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
