from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional
from datetime import datetime

class PatientBase(BaseModel):
    full_name: str = Field(..., max_length=100)
    age_months: int = Field(..., ge=0, le=72, description="Age in completed months")
    sex: Literal["M", "F"]
    weight: Optional[float] = Field(None, gt=0, le=150)
    height: Optional[float] = Field(None, gt=0, le=250)
    guardian_name: Optional[str] = Field(None, max_length=100)

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    age_months: Optional[int] = Field(None, ge=0, le=72)
    sex: Optional[Literal["M", "F"]] = None
    weight: Optional[float] = Field(None, gt=0, le=150)
    height: Optional[float] = Field(None, gt=0, le=250)
    guardian_name: Optional[str] = Field(None, max_length=100)
    active: Optional[bool] = None

class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str
    created_by: str
    active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

