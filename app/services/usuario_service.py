from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import usuario_schema
from app.repositories.usuario_repository import usuario as crud_usuario
from app.repositories.rol_repository import rol as crud_rol

def crear_usuario(db: Session, user_in: usuario_schema.UsuarioCreate):
    
    email_limpio = user_in.email.strip().lower()

    if len(user_in.password) < 8:
        raise BadRequestException(
            codigo_interno="ERR_PASSWORD_DEBIL",
            mensaje="Por políticas de seguridad, la contraseña debe tener al menos 8 caracteres."
        )

    rol_db = crud_rol.get(db=db, id=user_in.id_rol)
    if not rol_db:
        raise NotFoundException(
            codigo_interno="ERR_ROL_NO_ENCONTRADO",
            mensaje="El rol que intenta asignar a este usuario no existe en el sistema."
        )

    if crud_usuario.get_by_email(db, email=email_limpio):
        raise ConflictException(
            codigo_interno="ERR_EMAIL_DUPLICADO",
            mensaje="El correo especificado ya se encuentra registrado a nombre de otro usuario."
        )

    user_in.email = email_limpio
    return crud_usuario.create_user(db, obj_in=user_in.model_dump())


def obtener_usuarios_paginados(db: Session, page: int, page_size: int, email_filtro: Optional[str] = None, id_rol: Optional[int] = None):

    query = crud_usuario.obtener_query_filtrada(db, email_filtro=email_filtro, id_rol=id_rol)
    return paginar_resultados(db, crud_usuario, page, page_size, query_personalizada=query)


def actualizar_usuario(db: Session, id_user: int, user_in: usuario_schema.UsuarioUpdate):

    usuario_actual = crud_usuario.get(db=db, id=id_user)
    if not usuario_actual:
        raise NotFoundException(codigo_interno="ERR_NO_EXISTE", mensaje="Usuario no encontrado en el sistema.")

    update_data = user_in.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_limpio = update_data["email"].strip().lower()
        user_dup = crud_usuario.get_by_email(db, email=email_limpio)
        if user_dup and user_dup.id_user != id_user:
            raise ConflictException(
                codigo_interno="ERR_EMAIL_DUPLICADO", 
                mensaje="El correo ingresado ya pertenece a otra cuenta."
            )
        update_data["email"] = email_limpio

    if "id_rol" in update_data:
        rol_db = crud_rol.get(db=db, id=update_data["id_rol"])
        if not rol_db:
            raise NotFoundException(
                codigo_interno="ERR_ROL_NO_ENCONTRADO",
                mensaje="El nuevo rol asignado no existe."
            )
    return crud_usuario.update(db=db, db_obj=usuario_actual, obj_in=update_data)