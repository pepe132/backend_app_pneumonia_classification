import uuid
import math
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.patients.models import Patient
from app.modules.patients import schema

def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    return (
        db.query(Patient)
        .filter(Patient.active == True)
        .order_by(Patient.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_patient_by_id(
    db: Session,
    patient_id: str,
    *,
    include_inactive: bool = False,
) -> Optional[Patient]:
    query = db.query(Patient).filter(Patient.patient_id == patient_id)
    if not include_inactive:
        query = query.filter(Patient.active == True)
    return query.first()

def create_patient(db: Session, patient_data: schema.PatientCreate, user_id: str) -> Patient:
    new_patient = Patient(
        patient_id=str(uuid.uuid4()),
        full_name=patient_data.full_name,
        age_months=patient_data.age_months,
        sex=patient_data.sex,
        weight=patient_data.weight,
        height=patient_data.height,
        guardian_name=patient_data.guardian_name,
        created_by=user_id,
        active=True
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

def update_patient(db: Session, patient_id: str, patient_data: schema.PatientUpdate) -> Optional[Patient]:
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return None
    
    update_data = patient_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: str) -> bool:
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return False
    
    db_patient.active = False
    db.commit()
    return True

def search_patients(db: Session, query: str) -> List[Patient]:
    return db.query(Patient).filter(
        Patient.full_name.ilike(f"%{query}%"),
        Patient.active == True
    ).all()


def get_patients_page(
    db: Session,
    *,
    page: int,
    page_size: int,
    search: str | None = None,
    sex: str | None = None,
    active: bool | None = True,
    min_age_months: int | None = None,
    max_age_months: int | None = None,
    created_by: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict:
    query = db.query(Patient)
    if search:
        query = query.filter(Patient.full_name.ilike(f"%{search.strip()}%"))
    if sex:
        query = query.filter(Patient.sex == sex)
    if active is not None:
        query = query.filter(Patient.active == active)
    if min_age_months is not None:
        query = query.filter(Patient.age_months >= min_age_months)
    if max_age_months is not None:
        query = query.filter(Patient.age_months <= max_age_months)
    if created_by:
        query = query.filter(Patient.created_by == created_by)
    if date_from:
        query = query.filter(Patient.created_at >= date_from)
    if date_to:
        query = query.filter(Patient.created_at <= date_to)

    total = query.count()
    column = getattr(Patient, sort_by)
    query = query.order_by(column.asc() if sort_order == "asc" else column.desc())
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": math.ceil(total / page_size) if total else 0,
    }
