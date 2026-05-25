from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.auth import schema, service


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def build_user_response(user):
    return {
        "user_id": user.user_id,
        "user_name": user.user_name,
        "email": user.email,
        "role_id": user.role_id,
        "active": user.active,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "role_name": user.role.role_name if user.role else None
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = service.get_current_user_from_payload(db, payload)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/register", response_model=schema.UserResponse)
def register(user_data: schema.RegisterRequest, db: Session = Depends(get_db)):
    if user_data.role_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No está permitido registrar usuarios administradores desde este endpoint"
        )

    role = service.get_role_by_id(db, user_data.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol especificado no existe"
        )

    if service.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    user = service.register_user(db, user_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo registrar el usuario"
        )

    return build_user_response(user)


@router.post("/login", response_model=schema.TokenResponse)
def login(login_data: schema.LoginRequest, db: Session = Depends(get_db)):
    user = service.authenticate_user(db, login_data)

    if not user:
        db_user = service.get_user_by_email(db, login_data.email)

        if db_user and not db_user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La cuenta de usuario está inactiva"
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = service.create_user_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": build_user_response(user)
    }


@router.get("/me", response_model=schema.CurrentUserResponse)
def get_me(current_user=Depends(get_current_user)):
    return build_user_response(current_user)