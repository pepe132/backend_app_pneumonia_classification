from datetime import datetime
from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

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


@router.get("/page", response_model=schema.PatientPage)
def list_patients_page(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, min_length=1, max_length=100),
    sex: Literal["M", "F"] | None = None,
    active: bool | None = True,
    min_age_months: int | None = Query(None, ge=0, le=72),
    max_age_months: int | None = Query(None, ge=0, le=72),
    created_by: str | None = Query(None, max_length=40),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort_by: Literal["full_name", "age_months", "created_at", "updated_at"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if min_age_months is not None and max_age_months is not None and min_age_months > max_age_months:
        raise HTTPException(status_code=422, detail="El rango de edad no es válido")
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=422, detail="El rango de fechas no es válido")
    return service.get_patients_page(
        db,
        page=page,
        page_size=page_size,
        search=search,
        sex=sex,
        active=active,
        min_age_months=min_age_months,
        max_age_months=max_age_months,
        created_by=created_by,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        sort_order=sort_order,
    )

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
