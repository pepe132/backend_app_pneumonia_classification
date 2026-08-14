from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.modules.auth.router import get_current_user
from app.modules.evaluations import service as evaluation_service
from app.modules.radiographs import schema, service
from app.modules.radiographs.predictor import ImageModelUnavailableError


router = APIRouter(prefix="/evaluations", tags=["Radiographs"])


@router.post(
    "/{evaluation_id}/radiograph",
    response_model=schema.RadiographAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_radiograph(
    evaluation_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([1, 2])),
):
    evaluation = evaluation_service.get_evaluation_by_id(db, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    try:
        return await service.analyze_radiograph(
            db=db,
            evaluation=evaluation,
            upload=file,
            user_id=current_user.user_id,
        )
    except service.RadiographAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except service.InvalidRadiographError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ImageModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get(
    "/{evaluation_id}/radiograph",
    response_model=schema.RadiographResponse,
)
def get_radiograph(
    evaluation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    evaluation = evaluation_service.get_evaluation_by_id(db, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    radiograph = service.get_radiograph_by_evaluation(db, evaluation_id)
    if not radiograph:
        raise HTTPException(status_code=404, detail="Radiografía no encontrada")

    return service.serialize_radiograph(radiograph)
