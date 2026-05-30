from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import usuario_schema
from app.db.database import get_db 
from app.services import usuario_service
from app.api.dependencies import VerificarRol, ADMIN

router = APIRouter()

@router.post("/", response_model=usuario_schema.UsuarioResponse, summary="Crear usuario", dependencies=[Depends(VerificarRol([ADMIN]))])
def create_user(*, db: Session = Depends(get_db), user_in: usuario_schema.UsuarioCreate):
    return usuario_service.crear_usuario(db=db, user_in=user_in)

@router.get("/", response_model=usuario_schema.UsuarioPaginatedResponse, summary="Obtener usuarios", dependencies=[Depends(VerificarRol([ADMIN]))])
def read_users(
    email: Optional[str] = None, 
    id_rol: Optional[int] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return usuario_service.obtener_usuarios_paginados(db=db, page=page, page_size=page_size, email_filtro=email, id_rol=id_rol)

@router.patch("/{id_user}", response_model=usuario_schema.UsuarioResponse, summary="Actualizar usuario", dependencies=[Depends(VerificarRol([ADMIN]))])
def update_user(*, db: Session = Depends(get_db), id_user: int, user_in: usuario_schema.UsuarioUpdate):
    return usuario_service.actualizar_usuario(db=db, id_user=id_user, user_in=user_in)