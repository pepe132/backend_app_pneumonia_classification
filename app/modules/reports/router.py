import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.router import get_current_user
from app.modules.evaluations import service as evaluation_service
from app.modules.patients import service as patient_service
from app.modules.radiographs import service as radiograph_service
from app.modules.reports.schema import EvaluationReportResponse


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/evaluations/{evaluation_id}", response_model=EvaluationReportResponse
)
def get_evaluation_report(
    evaluation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    evaluation = evaluation_service.get_evaluation_by_id(db, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    patient = patient_service.get_patient_by_id(
        db, evaluation.patient_id, include_inactive=True
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    radiograph = evaluation.radiograph
    auxiliary_decision = None
    if evaluation.auxiliary_decision_json:
        auxiliary_decision = json.loads(evaluation.auxiliary_decision_json)
    elif radiograph:
        auxiliary_decision = radiograph_service.build_auxiliary_decision(
            evaluation, radiograph
        )

    return {
        "report_version": "1.0",
        "generated_at": datetime.now(timezone.utc),
        "patient": patient,
        "evaluation": evaluation,
        "integrated_result": {
            "final_severity": evaluation.final_severity,
            "radiographic_support": evaluation.radiographic_support,
            "concordance": evaluation.concordance,
            "basis": evaluation.fusion_basis,
            "explanation": evaluation.fusion_explanation,
            "recommendation_code": evaluation.recommendation_code,
            "fusion_version": evaluation.fusion_version,
        },
        "radiograph": (
            radiograph_service.serialize_radiograph(radiograph)
            if radiograph
            else None
        ),
        "auxiliary_decision": auxiliary_decision,
    }
