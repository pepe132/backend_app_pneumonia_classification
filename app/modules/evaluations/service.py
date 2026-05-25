import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.evaluations.models import Evaluation
from app.modules.evaluations import schema
from app.modules.patients.models import Patient


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

    new_evaluation = Evaluation(
        evaluation_id=str(uuid.uuid4()),
        created_by=user_id,
        **evaluation_data.model_dump(),
    )
    db.add(new_evaluation)
    db.commit()
    db.refresh(new_evaluation)
    return new_evaluation
