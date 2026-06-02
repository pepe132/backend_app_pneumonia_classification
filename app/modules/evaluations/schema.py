from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EvaluationBase(BaseModel):
    patient_id: str = Field(..., max_length=40)
    edad_meses: int = Field(..., ge=0, le=216)
    peso_kg: float = Field(..., gt=0, le=150)
    fr: int = Field(..., ge=0, le=120)
    fc: int = Field(..., ge=0, le=250)
    temperatura_c: float = Field(..., ge=30, le=45)
    spo2: int = Field(..., ge=0, le=100)
    tiraje: bool = False
    aleteo_nasal: bool = False
    quejido_espiratorio: bool = False
    cianosis: bool = False
    apnea: bool = False
    rechazo_comer: bool = False
    vomita_todo: bool = False
    convulsiones: bool = False
    glasgow: int = Field(..., ge=3, le=15)
    desnutricion: bool = False
    antecedentes_cronicos: bool = False
    sibilancias: bool = False
    dias_sintomas: int = Field(..., ge=0, le=60)
    dias_fiebre: int = Field(..., ge=0, le=60)
    dias_tos: int = Field(..., ge=0, le=60)
    dias_dificultad_respiratoria: int = Field(..., ge=0, le=60)
    crepitantes: bool = False
    disminucion_murmullo_vesicular: bool = False
    dolor_toracico: bool = False


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationResponse(EvaluationBase):
    evaluation_id: str
    created_by: str
    severity_tabular: Optional[str] = None
    prob_low: Optional[float] = None
    prob_medium: Optional[float] = None
    prob_high: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
