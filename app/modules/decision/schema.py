from typing import Literal

from pydantic import BaseModel, Field


ClinicalPrediction = Literal["Low", "Moderate", "High"]
RadiographicPrediction = Literal[
    "COVID-19",
    "Normal",
    "Bacterial pneumonia",
    "Viral pneumonia",
]


class ClinicalProbabilities(BaseModel):
    Low: float = Field(..., ge=0, le=1)
    Moderate: float = Field(..., ge=0, le=1)
    High: float = Field(..., ge=0, le=1)


class ClinicalResult(BaseModel):
    prediction: ClinicalPrediction
    probabilities: ClinicalProbabilities


class XrayProbabilities(BaseModel):
    COVID_19: float = Field(..., ge=0, le=1, alias="COVID-19")
    Normal: float = Field(..., ge=0, le=1)
    Bacterial_pneumonia: float = Field(
        ...,
        ge=0,
        le=1,
        alias="Bacterial pneumonia",
    )
    Viral_pneumonia: float = Field(..., ge=0, le=1, alias="Viral pneumonia")


class XrayResult(BaseModel):
    prediction: RadiographicPrediction
    probabilities: XrayProbabilities


class PatientData(BaseModel):
    patient_id: str | None = Field(default=None, max_length=40)
    edad_meses: int = Field(..., ge=0, le=72)
    peso_kg: float | None = Field(default=None, gt=0, le=150)
    spo2: float = Field(..., ge=0, le=100)
    fr: float = Field(..., ge=0)
    fc: float = Field(..., ge=0)
    temperatura_c: float = Field(..., ge=30, le=45)
    tiraje: bool = False
    retraccion_xifoidea: bool = False
    disociacion_toracoabdominal: bool = False
    aleteo_nasal: bool = False
    quejido_espiratorio: bool = False
    cianosis: bool = False
    apnea: bool = False
    rechazo_comer: bool = False
    vomita_todo: bool = False
    convulsiones: bool = False
    glasgow: float = Field(..., ge=3, le=15)
    desnutricion: bool = False
    antecedentes_cronicos: bool = False
    sibilancias: bool = False
    dias_sintomas: int = Field(..., ge=0)
    dias_fiebre: int = Field(..., ge=0)
    dias_tos: int = Field(..., ge=0)
    dias_dificultad_respiratoria: int = Field(..., ge=0)
    crepitantes: bool = False
    disminucion_murmullo_vesicular: bool = False
    dolor_toracico: bool = False


class AuxiliaryDecisionRequest(BaseModel):
    clinical_result: ClinicalResult
    xray_result: XrayResult
    patient_data: PatientData


class AuxiliaryDecisionResponse(BaseModel):
    clasificacion_auxiliar: str
    prediccion_severidad: str
    probabilidades_severidad: dict[str, float]
    hallazgos_clinicos_relevantes: list[str]
    resultado_radiografico_auxiliar: str
    prediccion_radiografica: str
    probabilidades_radiograficas: dict[str, float]
    recomendacion: str
    nota_seguridad: str
