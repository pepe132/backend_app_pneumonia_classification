from datetime import datetime

from pydantic import BaseModel

from app.modules.decision.schema import AuxiliaryDecisionResponse
from app.modules.evaluations.schema import EvaluationResponse
from app.modules.patients.schema import PatientResponse
from app.modules.radiographs.schema import FusionResult, RadiographResponse


class EvaluationReportResponse(BaseModel):
    report_version: str
    generated_at: datetime
    patient: PatientResponse
    evaluation: EvaluationResponse
    integrated_result: FusionResult
    radiograph: RadiographResponse | None = None
    auxiliary_decision: AuxiliaryDecisionResponse | None = None

