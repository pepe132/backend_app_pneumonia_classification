import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import engine, get_db
from app.main import app


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def db_client(db_session):
    def override_get_db():
        try:
            yield db_session
        except Exception:
            db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def low_clinical_result():
    return {
        "prediction": "Low",
        "probabilities": {"Low": 0.80, "Moderate": 0.15, "High": 0.05},
    }


@pytest.fixture
def normal_xray_result():
    return {
        "prediction": "Normal",
        "probabilities": {
            "COVID-19": 0.02,
            "Normal": 0.90,
            "Bacterial pneumonia": 0.05,
            "Viral pneumonia": 0.03,
        },
    }


@pytest.fixture
def patient_data():
    return {
        "patient_id": "test-patient",
        "edad_meses": 36,
        "peso_kg": 14.0,
        "spo2": 97,
        "fr": 28,
        "fc": 105,
        "temperatura_c": 37.0,
        "tiraje": False,
        "retraccion_xifoidea": False,
        "disociacion_toracoabdominal": False,
        "aleteo_nasal": False,
        "quejido_espiratorio": False,
        "cianosis": False,
        "apnea": False,
        "rechazo_comer": False,
        "vomita_todo": False,
        "convulsiones": False,
        "glasgow": 15,
        "desnutricion": False,
        "antecedentes_cronicos": False,
        "sibilancias": False,
        "dias_sintomas": 2,
        "dias_fiebre": 0,
        "dias_tos": 2,
        "dias_dificultad_respiratoria": 0,
        "crepitantes": False,
        "disminucion_murmullo_vesicular": False,
        "dolor_toracico": False,
    }
