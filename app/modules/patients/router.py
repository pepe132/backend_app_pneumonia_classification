from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.modules.auth.router import get_current_user
from app.modules.patients import schema, service

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=schema.PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_data: schema.PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles([1, 2]))
):
    return service.create_patient(db, patient_data, current_user.user_id)

@router.get("/", response_model=List[schema.PatientResponse])
def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.get_patients(db, skip, limit)

@router.get("/search", response_model=List[schema.PatientResponse])
def search_patients(
    q: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.search_patients(db, q)

@router.get("/{patient_id}", response_model=schema.PatientResponse)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = service.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient

@router.patch("/{patient_id}", response_model=schema.PatientResponse)
def update_patient(
    patient_id: str,
    patient_data: schema.PatientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles([1, 2]))
):
    patient = service.update_patient(db, patient_id, patient_data)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles([1, 2]))
):
    success = service.delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return None
