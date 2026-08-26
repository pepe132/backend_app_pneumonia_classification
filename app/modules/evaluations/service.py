import uuid
import math
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.evaluations.models import Evaluation
from app.modules.evaluations import schema
from app.modules.evaluations.fusion import fuse_results
from app.modules.patients.models import Patient
from app.modules.evaluations.predictor import predict_tabular_severity


def get_evaluations(db: Session, skip: int = 0, limit: int = 100) -> List[Evaluation]:
    return (
        db.query(Evaluation)
        .order_by(Evaluation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_evaluation_by_id(db: Session, evaluation_id: str) -> Optional[Evaluation]:
    return db.query(Evaluation).filter(Evaluation.evaluation_id == evaluation_id).first()


def get_patient_evaluations(
    db: Session,
    patient_id: str,
    skip: int = 0,
    limit: int = 100,
) -> List[Evaluation]:
    return (
        db.query(Evaluation)
        .filter(Evaluation.patient_id == patient_id)
        .order_by(Evaluation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def patient_exists(db: Session, patient_id: str) -> bool:
    return (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id, Patient.active == True)
        .first()
        is not None
    )


def create_evaluation(
    db: Session,
    evaluation_data: schema.EvaluationCreate,
    user_id: str,
) -> Optional[Evaluation]:
    if not patient_exists(db, evaluation_data.patient_id):
        return None
    
    prediction = predict_tabular_severity(evaluation_data)
    integrated_result = fuse_results(prediction["severity_tabular"])

    new_evaluation = Evaluation(
        evaluation_id=str(uuid.uuid4()),
        created_by=user_id,
        **evaluation_data.model_dump(),
        severity_tabular=prediction["severity_tabular"],
        prob_low=prediction["prob_low"],
        prob_medium=prediction["prob_medium"],
        prob_high=prediction["prob_high"],
        final_severity=integrated_result["final_severity"],
        radiographic_support=integrated_result["radiographic_support"],
        concordance=integrated_result["concordance"],
        fusion_basis=integrated_result["basis"],
        fusion_explanation=integrated_result["explanation"],
        recommendation_code=integrated_result["recommendation_code"],
        fusion_version=integrated_result["fusion_version"],
    )
    db.add(new_evaluation)
    db.commit()
    db.refresh(new_evaluation)
    return new_evaluation


def get_evaluations_page(
    db: Session,
    *,
    page: int,
    page_size: int,
    patient_id: str | None = None,
    severity_tabular: str | None = None,
    final_severity: str | None = None,
    created_by: str | None = None,
    has_radiograph: bool | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict:
    query = db.query(Evaluation)
    if patient_id:
        query = query.filter(Evaluation.patient_id == patient_id)
    if severity_tabular:
        query = query.filter(Evaluation.severity_tabular == severity_tabular)
    if final_severity:
        query = query.filter(Evaluation.final_severity == final_severity)
    if created_by:
        query = query.filter(Evaluation.created_by == created_by)
    if has_radiograph is True:
        query = query.filter(Evaluation.radiograph.has())
    elif has_radiograph is False:
        query = query.filter(~Evaluation.radiograph.has())
    if date_from:
        query = query.filter(Evaluation.created_at >= date_from)
    if date_to:
        query = query.filter(Evaluation.created_at <= date_to)

    total = query.count()
    column = getattr(Evaluation, sort_by)
    query = query.order_by(column.asc() if sort_order == "asc" else column.desc())
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": math.ceil(total / page_size) if total else 0,
    }
