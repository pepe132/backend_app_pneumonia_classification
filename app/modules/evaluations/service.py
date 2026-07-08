import uuid
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
