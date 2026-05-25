import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.patients.models import Patient
from app.modules.patients import schema

def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    return db.query(Patient).filter(Patient.active == True).offset(skip).limit(limit).all()

def get_patient_by_id(db: Session, patient_id: str) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()

def create_patient(db: Session, patient_data: schema.PatientCreate, user_id: str) -> Patient:
    new_patient = Patient(
        patient_id=str(uuid.uuid4()),
        full_name=patient_data.full_name,
        age=patient_data.age,
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
