from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PatientBase(BaseModel):
    full_name: str = Field(..., max_length=100)
    age: int = Field(..., description="Age in months or years")
    sex: str = Field(..., max_length=10)
    weight: Optional[float] = None
    height: Optional[float] = None
    guardian_name: Optional[str] = Field(None, max_length=100)

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = None
    sex: Optional[str] = Field(None, max_length=10)
    weight: Optional[float] = None
    height: Optional[float] = None
    guardian_name: Optional[str] = Field(None, max_length=100)
    active: Optional[bool] = None

class PatientResponse(PatientBase):
    patient_id: str
    created_by: str
    active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
