from fastapi import Depends, HTTPException, status
from typing import List
from app.modules.auth.router import get_current_user # Temp import to keep things working or I can move logic here

def require_roles(allowed_roles: List[int]):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para realizar esta acción"
            )
        return current_user
    return role_checker
