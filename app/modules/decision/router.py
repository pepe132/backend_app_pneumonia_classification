from fastapi import APIRouter, HTTPException, status

from app.modules.decision.schema import AuxiliaryDecisionRequest
from app.services.auxiliary_decision import generate_auxiliary_decision


router = APIRouter(prefix="/decision", tags=["Decision"])


@router.post("/auxiliary", status_code=status.HTTP_200_OK)
def create_auxiliary_decision(request: AuxiliaryDecisionRequest):
    try:
        return generate_auxiliary_decision(
            clinical_result=request.clinical_result.model_dump(by_alias=True),
            xray_result=request.xray_result.model_dump(by_alias=True),
            patient_data=request.patient_data.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error inesperado al generar la decisión auxiliar",
        ) from exc
