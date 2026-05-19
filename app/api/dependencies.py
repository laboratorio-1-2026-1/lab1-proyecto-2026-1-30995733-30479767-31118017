from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import ALGORITHM, SECRET_KEY
from app.crud.crud_usuario import usuario as crud_usuario
from app.models.usuario import Usuario


bearer_scheme = HTTPBearer()

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = crud_usuario.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user