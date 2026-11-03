from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import decode_access_token
from app.modules.auth import schema, service


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


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


def build_token_response(user):
    access_token = service.create_user_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": build_user_response(user)
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


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos suficientes para realizar esta acción",
        )
    return current_user


def validate_login(db: Session, login_data: schema.LoginRequest):
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

    return user


@router.post("/register", response_model=schema.UserResponse)
def register(user_data: schema.RegisterRequest, db: Session = Depends(get_db)):
    if not settings.allow_public_registration:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El registro público de usuarios está deshabilitado",
        )
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
    user = validate_login(db, login_data)
    return build_token_response(user)


@router.post("/token", response_model=schema.TokenResponse)
async def token(request: Request, db: Session = Depends(get_db)):
    form_data = parse_qs((await request.body()).decode())

    login_data = schema.LoginRequest(
        email=form_data.get("username", [""])[0],
        user_password=form_data.get("password", [""])[0]
    )

    user = validate_login(db, login_data)
    return build_token_response(user)


@router.get("/me", response_model=schema.CurrentUserResponse)
def get_me(current_user=Depends(get_current_user)):
    return build_user_response(current_user)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    password_data: schema.PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not service.verify_password(
        password_data.current_password, current_user.user_password
    ):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
    if service.verify_password(password_data.new_password, current_user.user_password):
        raise HTTPException(
            status_code=409, detail="La nueva contraseña debe ser diferente"
        )
    service.set_user_password(db, current_user, password_data.new_password)
    return None


@router.get("/users", response_model=list[schema.UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return [build_user_response(user) for user in service.get_users(db, skip, limit)]


@router.get("/users/{user_id}", response_model=schema.UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return build_user_response(user)


@router.post(
    "/users", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: schema.AdminUserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    if service.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=409, detail="El correo ya está registrado")
    if not service.get_role_by_id(db, user_data.role_id):
        raise HTTPException(status_code=400, detail="El rol especificado no existe")
    return build_user_response(service.create_user_by_admin(db, user_data))


@router.patch("/users/{user_id}", response_model=schema.UserResponse)
def update_user(
    user_id: str,
    user_data: schema.AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user_data.email is not None:
        existing = service.get_user_by_email(db, user_data.email)
        if existing and existing.user_id != user_id:
            raise HTTPException(status_code=409, detail="El correo ya está registrado")
    if user_data.role_id is not None and not service.get_role_by_id(db, user_data.role_id):
        raise HTTPException(status_code=400, detail="El rol especificado no existe")
    if user_id == current_user.user_id and (
        user_data.active is False or user_data.role_id not in (None, 1)
    ):
        raise HTTPException(
            status_code=409,
            detail="Un administrador no puede desactivar ni retirar su propio rol",
        )
    return build_user_response(service.update_user_by_admin(db, user, user_data))


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=409, detail="Un administrador no puede desactivarse a sí mismo"
        )
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    service.update_user_by_admin(db, user, schema.AdminUserUpdate(active=False))
    return None


@router.post(
    "/users/{user_id}/reset-password", status_code=status.HTTP_204_NO_CONTENT
)
def reset_user_password(
    user_id: str,
    password_data: schema.PasswordResetRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if service.verify_password(password_data.new_password, user.user_password):
        raise HTTPException(
            status_code=409, detail="La nueva contraseña debe ser diferente"
        )
    service.set_user_password(db, user, password_data.new_password)
    return None
