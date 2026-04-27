from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.core.config import APP_NAME, APP_VERSION

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