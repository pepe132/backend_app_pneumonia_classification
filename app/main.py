from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.core.config import APP_NAME, APP_VERSION
from app.modules.auth.router import router as auth_router
from app.modules.evaluations.router import router as evaluations_router
from app.modules.patients.router import router as patients_router
from app.modules.radiographs.router import router as radiographs_router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
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
