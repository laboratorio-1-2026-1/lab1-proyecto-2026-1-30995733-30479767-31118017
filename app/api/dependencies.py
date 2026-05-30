from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.core.config import settings 
from app.repositories.usuario_repository import usuario as crud_usuario
from app.models.usuario_model import Usuario

bearer_scheme = HTTPBearer()

ADMIN = 1
FINANZAS = 2
ENTRENADOR = 3
CLIENTE = 4

def get_current_user(
    db: Session = Depends(get_db), 
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme) 
) -> Usuario:

    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o token inválido.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = crud_usuario.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user

class VerificarRol:

    def __init__(self, roles_permitidos: List[int]):
        self.roles_permitidos = roles_permitidos

    def __call__(self, current_user: Usuario = Depends(get_current_user)):
        if current_user.id_rol not in self.roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios (Rol inadecuado) para realizar esta acción."
            )
        return current_user