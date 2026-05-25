import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.auth.models import User, Role
from app.modules.auth import schema
from app.core.security import hash_password, verify_password, create_access_token

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()

def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.role_id == role_id).first()

def register_user(db: Session, user_data: schema.RegisterRequest) -> Optional[User]:
    # Validación: No permitir registro público con role_id = 1 (Admin/Especial)
    if user_data.role_id == 1:
        return None
    
    # Verificar si el email ya existe
    if get_user_by_email(db, user_data.email):
        return None

    # Crear nuevo usuario con UUID
    new_user = User(
        user_id=str(uuid.uuid4()),
        user_name=user_data.user_name,
        email=user_data.email,
        user_password=hash_password(user_data.user_password),
        role_id=user_data.role_id,
        active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, login_data: schema.LoginRequest) -> Optional[User]:
    user = get_user_by_email(db, login_data.email)
    
    if not user:
        return None
    
    if not verify_password(login_data.user_password, user.user_password):
        return None
    
    # No permitir login si el usuario está inactivo
    if not user.active:
        return None
        
    return user

def create_user_token(user: User) -> str:
    """Genera el token JWT con el payload solicitado."""
    token_data = {
        "sub": user.user_id,
        "email": user.email,
        "role_id": user.role_id
    }
    return create_access_token(data=token_data)

def get_current_user_from_payload(db: Session, payload: dict) -> Optional[User]:
    """Obtiene el usuario a partir del payload decodificado del token."""
    user_id = payload.get("sub")
    if not user_id:
        return None
    return get_user_by_id(db, user_id)
