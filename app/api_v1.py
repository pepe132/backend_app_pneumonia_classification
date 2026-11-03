from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.decision.router import router as decision_router
from app.modules.evaluations.router import router as evaluations_router
from app.modules.patients.router import router as patients_router
from app.modules.radiographs.router import router as radiographs_router
from app.modules.reports.router import router as reports_router


router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(patients_router)
router.include_router(evaluations_router)
router.include_router(radiographs_router)
router.include_router(decision_router)
router.include_router(reports_router)
router.include_router(dashboard_router)
