from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.modules.auth.router import get_current_user
from app.modules.evaluations import schema, service

router = APIRouter(tags=["Evaluations"])


@router.post("/evaluations", response_model=schema.EvaluationResponse, status_code=status.HTTP_201_CREATED)
def create_evaluation(
    evaluation_data: schema.EvaluationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([1, 2])),
):
    evaluation = service.create_evaluation(db, evaluation_data, current_user.user_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return evaluation


@router.get("/evaluations", response_model=List[schema.EvaluationResponse])
def list_evaluations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_evaluations(db, skip, limit)


@router.get("/evaluations/{evaluation_id}", response_model=schema.EvaluationResponse)
def get_evaluation(
    evaluation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    evaluation = service.get_evaluation_by_id(db, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluacion no encontrada")
    return evaluation


@router.get("/patients/{patient_id}/evaluations", response_model=List[schema.EvaluationResponse])
def list_patient_evaluations(
    patient_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not service.patient_exists(db, patient_id):
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return service.get_patient_evaluations(db, patient_id, skip, limit)
