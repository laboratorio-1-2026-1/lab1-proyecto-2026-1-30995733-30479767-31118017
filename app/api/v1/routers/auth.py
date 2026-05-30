from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.database import get_db
from app.services import auth_service

router = APIRouter()

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    id_rol: int
    id_user: int

@router.post("/login", response_model=TokenResponse)
def login_access_token(
    user_credentials: UsuarioLogin,
    db: Session = Depends(get_db)
):
    return auth_service.autenticar_usuario(
        db=db, 
        email=user_credentials.email, 
        password=user_credentials.password
    )