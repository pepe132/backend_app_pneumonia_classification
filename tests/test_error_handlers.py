from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.core import database
from app.core.error_handlers import register_error_handlers


def test_http_errors_use_uniform_contract():
    from app.main import app

    client = TestClient(app)
    response = client.get("/patients/")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {
        "error": {
            "code": "AUTHENTICATION_REQUIRED",
            "message": "No se proporcionaron credenciales de autenticación",
        }
    }


def test_database_errors_do_not_expose_internal_details():
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/database-error")
    def database_error():
        raise OperationalError(
            "SELECT secret FROM private_table",
            {"password": "hidden"},
            RuntimeError("driver failure"),
        )

    response = TestClient(app, raise_server_exceptions=False).get("/database-error")

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "DATABASE_UNAVAILABLE",
            "message": "No fue posible completar la operación en la base de datos",
        }
    }
    assert "secret" not in response.text
    assert "password" not in response.text


def test_unexpected_errors_return_generic_message():
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/unexpected")
    def unexpected():
        raise RuntimeError("sensitive internal detail")

    response = TestClient(app, raise_server_exceptions=False).get("/unexpected")

    assert response.status_code == 500
    assert response.json()["error"] == {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Ocurrió un error interno inesperado",
    }
    assert "sensitive" not in response.text


def test_database_dependency_rolls_back_and_closes(monkeypatch):
    class FakeSession:
        def __init__(self):
            self.rolled_back = False
            self.closed = False

        def rollback(self):
            self.rolled_back = True

        def close(self):
            self.closed = True

    session = FakeSession()
    monkeypatch.setattr(database, "SessionLocal", lambda: session)
    dependency = database.get_db()

    assert next(dependency) is session
    try:
        dependency.throw(RuntimeError("request failed"))
    except RuntimeError:
        pass

    assert session.rolled_back
    assert session.closed
