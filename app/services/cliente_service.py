from fastapi import status
from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.utils import paginar_resultados
from app.schemas import cliente_schema
from app.repositories.cliente_repository import cliente as crud_cliente
from app.repositories.usuario_repository import usuario as crud_usuario

def crear_cliente(db: Session, cliente_in: cliente_schema.ClienteCreate):

    nombre_limpio = cliente_in.nombre_cli.strip().title()
    apellido_limpio = cliente_in.apellido_cli.strip().title()
    cedula_limpia = cliente_in.cedula.strip().upper()

    if not nombre_limpio or not apellido_limpio or not cedula_limpia:
        raise BadRequestException(
            codigo_interno="ERR_DATOS_VACIOS",
            mensaje="Los campos nombre, apellido y cédula son obligatorios."
        )

    if len(cedula_limpia) < 6 or not cedula_limpia.isalnum():
        raise BadRequestException(
            codigo_interno="ERR_CEDULA_INVALIDA",
            mensaje="La cédula debe ser alfanumérica y contener al menos 6 caracteres."
        )

    usuario_db = crud_usuario.get(db=db, id=cliente_in.id_usuario)
    if not usuario_db:
        raise NotFoundException(
            codigo_interno="ERR_USUARIO_NO_ENCONTRADO",
            mensaje="El ID de usuario especificado no existe en el sistema."
        )

    if usuario_db.id_rol != 4:
        raise ConflictException(
            codigo_interno="ERR_ROL_INVALIDO",
            mensaje="Incongruencia de datos: El usuario debe poseer el rol de Cliente (Rol 4) para crearle un perfil."
        )

    if crud_cliente.get_by_usuario_id(db=db, id_usuario=cliente_in.id_usuario):
        raise ConflictException(
            codigo_interno="ERR_PERFIL_DUPLICADO",
            mensaje="El usuario especificado ya posee un perfil de cliente asociado."
        )

    if crud_cliente.get_by_cedula(db=db, cedula=cedula_limpia):
        raise ConflictException(
            codigo_interno="ERR_CEDULA_DUPLICADA",
            mensaje=f"Ya existe un cliente registrado con la cédula {cedula_limpia}."
        )

    cliente_in.nombre_cli = nombre_limpio
    cliente_in.apellido_cli = apellido_limpio
    cliente_in.cedula = cedula_limpia
    return crud_cliente.create(db, obj_in=cliente_in.model_dump())

def obtener_clientes_paginados(db: Session, page: int, page_size: int, cedula: Optional[str] = None):
    query = crud_cliente.obtener_query_filtrada(db, cedula=cedula)
    return paginar_resultados(db, crud_cliente, page, page_size, query_personalizada=query)

def actualizar_cliente(db: Session, id_cliente: int, cliente_in: cliente_schema.ClienteUpdate):

    cliente_actual = crud_cliente.get(db=db, id=id_cliente)
    if not cliente_actual:
        raise NotFoundException(codigo_interno="ERR_NO_EXISTE", mensaje="Cliente no encontrado.")

    update_data = cliente_in.model_dump(exclude_unset=True)

    if "nombre_cli" in update_data:
        nombre_limpio = update_data["nombre_cli"].strip().title()
        if not nombre_limpio:
            raise BadRequestException(codigo_interno="ERR_DATOS_VACIOS", mensaje="El nombre no puede quedar vacío.")
        update_data["nombre_cli"] = nombre_limpio

    if "apellido_cli" in update_data:
        apellido_limpio = update_data["apellido_cli"].strip().title()
        if not apellido_limpio:
            raise BadRequestException(codigo_interno="ERR_DATOS_VACIOS", mensaje="El apellido no puede quedar vacío.")
        update_data["apellido_cli"] = apellido_limpio

    if "cedula" in update_data:
        cedula_limpia = update_data["cedula"].strip().upper()
        if not cedula_limpia or len(cedula_limpia) < 6 or not cedula_limpia.isalnum():
            raise BadRequestException(codigo_interno="ERR_CEDULA_INVALIDA", mensaje="La cédula debe ser alfanumérica y contener al menos 6 caracteres.")

        ced_existente = crud_cliente.get_by_cedula(db=db, cedula=cedula_limpia)
        if ced_existente and ced_existente.id_cliente != id_cliente:
            raise ConflictException(codigo_interno="ERR_CEDULA_DUPLICADA", mensaje="La cédula ingresada ya pertenece a otro cliente.")
        
        update_data["cedula"] = cedula_limpia
    return crud_cliente.update(db=db, db_obj=cliente_actual, obj_in=update_data)