from fastapi import Depends, HTTPException, status
from typing import List
from app.modules.auth.router import get_current_user # Temp import to keep things working or I can move logic here

# Politica de acceso clinico (2026-08-23): todos los usuarios autenticados
# pueden consultar la informacion clinica global. Las mutaciones permanecen
# restringidas por require_roles a administrador y especialista.
CLINICAL_READ_ROLE_IDS = (1, 2, 3)
CLINICAL_WRITE_ROLE_IDS = (1, 2)

def require_roles(allowed_roles: List[int]):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para realizar esta acción"
            )
        return current_user
    return role_checker
