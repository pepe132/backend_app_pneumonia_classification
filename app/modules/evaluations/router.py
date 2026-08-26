import json
from datetime import datetime
from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.modules.auth.router import get_current_user
from app.modules.evaluations import schema, service
from app.modules.decision.schema import AuxiliaryDecisionResponse
from app.modules.radiographs import service as radiograph_service

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


@router.get("/evaluations/page", response_model=schema.EvaluationPage)
def list_evaluations_page(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: str | None = Query(None, max_length=40),
    severity_tabular: Literal["Bajo", "Medio", "Alto"] | None = None,
    final_severity: Literal["Bajo", "Medio", "Alto"] | None = None,
    created_by: str | None = Query(None, max_length=40),
    has_radiograph: bool | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort_by: Literal["created_at", "severity_tabular", "final_severity"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=422, detail="El rango de fechas no es válido")
    return service.get_evaluations_page(
        db,
        page=page,
        page_size=page_size,
        patient_id=patient_id,
        severity_tabular=severity_tabular,
        final_severity=final_severity,
        created_by=created_by,
        has_radiograph=has_radiograph,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/evaluations/{evaluation_id}", response_model=schema.EvaluationResponse)
def get_evaluation(
    evaluation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    evaluation = service.get_evaluation_by_id(db, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
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


@router.get(
    "/evaluations/{evaluation_id}/auxiliary-decision",
    response_model=AuxiliaryDecisionResponse,
)
def get_evaluation_auxiliary_decision(
    evaluation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    evaluation = service.get_evaluation_by_id(db, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    if evaluation.auxiliary_decision_json:
        return json.loads(evaluation.auxiliary_decision_json)
    if evaluation.radiograph:
        return radiograph_service.build_auxiliary_decision(
            evaluation, evaluation.radiograph
        )
    raise HTTPException(
        status_code=404,
        detail="La evaluación no tiene una decisión auxiliar disponible",
    )
