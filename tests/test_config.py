import pytest
from pydantic import ValidationError

from app.core.config import Settings, parse_cors_origins


def settings_payload(**overrides):
    return {
        "db_server": "localhost",
        "db_name": "test_db",
        "db_user": "test_user",
        "db_password": "test_password",
        "secret_key": "development-secret",
        **overrides,
    }


def test_development_settings_keep_safe_defaults():
    settings = Settings(**settings_payload())

    assert settings.app_env == "development"
    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.cors_origins == []


def test_cors_origins_accept_comma_separated_or_json_list():
    assert parse_cors_origins("http://localhost:3000,http://localhost:5173") == [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    assert parse_cors_origins('["https://app.example.com"]') == [
        "https://app.example.com"
    ]


@pytest.mark.parametrize(
    "overrides",
    [
        {"app_env": "production", "secret_key": "short"},
        {
            "app_env": "production",
            "secret_key": "a" * 32,
            "debug": True,
        },
        {
            "app_env": "production",
            "secret_key": "a" * 32,
            "cors_origins": ["*"],
        },
        {
            "app_env": "production",
            "secret_key": "cambia-este-valor-por-una-clave-segura",
        },
    ],
)
def test_production_rejects_insecure_configuration(overrides):
    with pytest.raises(ValidationError):
        Settings(**settings_payload(**overrides))


def test_production_accepts_explicit_secure_configuration():
    settings = Settings(
        **settings_payload(
            app_env="production",
            secret_key="a-secure-production-secret-key-123456",
            debug=False,
            enable_docs=False,
            cors_origins=["https://app.example.com"],
        )
    )

    assert settings.app_env == "production"
    assert settings.enable_docs is False
    assert settings.cors_origins == ["https://app.example.com"]


@pytest.mark.parametrize("field", ["db_server", "db_name", "db_user", "db_password", "secret_key"])
def test_required_configuration_rejects_blank_values(field):
    with pytest.raises(ValidationError):
        Settings(**settings_payload(**{field: " "}))


def test_operational_limits_are_validated():
    with pytest.raises(ValidationError):
        Settings(**settings_payload(access_token_expire_minutes=0))
    with pytest.raises(ValidationError):
        Settings(**settings_payload(radiograph_max_size_mb=101))
    with pytest.raises(ValidationError):
        Settings(**settings_payload(cnn_min_confidence=1.1))
