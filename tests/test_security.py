from datetime import timedelta

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verification():
    password = "PruebaSegura_2026!"
    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("incorrecta", password_hash)


def test_access_token_round_trip():
    token = create_access_token({"sub": "test-user", "role_id": 2})
    payload = decode_access_token(token)

    assert payload["sub"] == "test-user"
    assert payload["role_id"] == 2


def test_expired_or_invalid_token_is_rejected():
    expired = create_access_token(
        {"sub": "test-user"},
        expires_delta=timedelta(seconds=-1),
    )

    assert decode_access_token(expired) is None
    assert decode_access_token("not-a-token") is None
