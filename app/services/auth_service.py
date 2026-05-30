from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.usuario_repository import usuario as crud_usuario
from app.core.security import create_access_token, verify_password

def autenticar_usuario(db: Session, email: str, password: str):

    user = crud_usuario.get_by_email(db, email=email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas. Verifique su correo electrónico y contraseña.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "id_user": user.id_user,
            "id_rol": user.id_rol
        }
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "id_rol": user.id_rol,
        "id_user": user.id_user
    }