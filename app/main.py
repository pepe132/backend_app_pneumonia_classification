from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.database import engine
from app.core.error_handlers import register_error_handlers
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.modules.auth.router import router as auth_router
from app.modules.decision.router import router as decision_router
from app.modules.evaluations.router import router as evaluations_router
from app.modules.patients.router import router as patients_router
from app.modules.radiographs.router import router as radiographs_router


configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

register_error_handlers(app)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

@app.get("/")
def root():
    return {"message": "API funcionando con SQL Server y pymssql"}

@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}

app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(evaluations_router)
app.include_router(radiographs_router)
app.include_router(decision_router)
