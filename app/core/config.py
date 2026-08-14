import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, model_validator


load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
INSECURE_SECRET_KEYS = {
    "your-super-secret-key-here",
    "cambia-este-valor-por-una-clave-segura",
}


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_cors_origins(value: str | list[str] | None) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value

    stripped = value.strip()
    if stripped.startswith("["):
        parsed = json.loads(stripped)
        if not isinstance(parsed, list):
            raise ValueError("CORS_ORIGINS debe ser una lista JSON o valores separados por coma")
        return [str(origin).strip() for origin in parsed if str(origin).strip()]
    return [origin.strip() for origin in stripped.split(",") if origin.strip()]


class Settings(BaseModel):
    app_name: str = "Neumonia Platform"
    app_version: str = "1.0.0"
    app_env: Literal["development", "testing", "production"] = "development"
    debug: bool = False
    enable_docs: bool = True
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    cors_origins: list[str] = Field(default_factory=list)

    db_server: str
    db_port: str = "1433"
    db_name: str
    db_user: str
    db_password: str
    db_driver: str = "ODBC Driver 18 for SQL Server"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, gt=0, le=1440)

    cnn_model_path: str = str(
        BASE_DIR / "modules" / "radiographs" / "densenet121_clahe_finetuned_model.keras"
    )
    radiograph_upload_dir: str = str(BASE_DIR / "uploads" / "radiographs")
    radiograph_max_size_mb: int = Field(default=10, gt=0, le=100)
    cnn_min_confidence: float = Field(default=0.60, ge=0, le=1)

    @field_validator(
        "db_server",
        "db_name",
        "db_user",
        "db_password",
        "secret_key",
    )
    @classmethod
    def required_strings_must_not_be_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("El valor no puede estar vacío")
        return value.strip()

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, value):
        return parse_cors_origins(value)

    @model_validator(mode="after")
    def validate_environment_security(self):
        if self.app_env == "production":
            if self.debug:
                raise ValueError("DEBUG no puede estar habilitado en producción")
            if self.secret_key in INSECURE_SECRET_KEYS or len(self.secret_key) < 32:
                raise ValueError(
                    "SECRET_KEY debe ser segura y tener al menos 32 caracteres en producción"
                )
            if "*" in self.cors_origins:
                raise ValueError("CORS_ORIGINS no puede contener '*' en producción")
        return self

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", "Neumonia Platform"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            app_env=os.getenv("APP_ENV", "development").lower(),
            debug=_env_bool("DEBUG", False),
            enable_docs=_env_bool("ENABLE_DOCS", True),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            cors_origins=os.getenv("CORS_ORIGINS", ""),
            db_server=os.getenv("DB_SERVER", ""),
            db_port=os.getenv("DB_PORT", "1433"),
            db_name=os.getenv("DB_NAME", ""),
            db_user=os.getenv("DB_USER", ""),
            db_password=os.getenv("DB_PASSWORD", ""),
            db_driver=os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server"),
            secret_key=os.getenv("SECRET_KEY", ""),
            algorithm=os.getenv("ALGORITHM", "HS256"),
            access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"),
            cnn_model_path=os.getenv(
                "CNN_MODEL_PATH",
                str(BASE_DIR / "modules" / "radiographs" / "densenet121_clahe_finetuned_model.keras"),
            ),
            radiograph_upload_dir=os.getenv(
                "RADIOGRAPH_UPLOAD_DIR",
                str(BASE_DIR / "uploads" / "radiographs"),
            ),
            radiograph_max_size_mb=os.getenv("RADIOGRAPH_MAX_SIZE_MB", "10"),
            cnn_min_confidence=os.getenv("CNN_MIN_CONFIDENCE", "0.60"),
        )


settings = Settings.from_environment()

# Compatibility aliases used by the existing modules.
APP_NAME = settings.app_name
APP_VERSION = settings.app_version
APP_ENV = settings.app_env
DEBUG = settings.debug
ENABLE_DOCS = settings.enable_docs
LOG_LEVEL = settings.log_level
CORS_ORIGINS = settings.cors_origins
DB_SERVER = settings.db_server
DB_PORT = settings.db_port
DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASSWORD = settings.db_password
DB_DRIVER = settings.db_driver
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
CNN_MODEL_PATH = settings.cnn_model_path
RADIOGRAPH_UPLOAD_DIR = settings.radiograph_upload_dir
RADIOGRAPH_MAX_SIZE_MB = settings.radiograph_max_size_mb
CNN_MIN_CONFIDENCE = settings.cnn_min_confidence
