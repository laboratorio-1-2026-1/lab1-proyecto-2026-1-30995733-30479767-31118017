from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import cliente_schema
from app.db.database import get_db
from app.services import cliente_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=cliente_schema.ClienteResponse, summary="Crear cliente", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_cliente(*, db: Session = Depends(get_db), cliente_in: cliente_schema.ClienteCreate):
    return cliente_service.crear_cliente(db=db, cliente_in=cliente_in)

@router.get("/", response_model=cliente_schema.ClientePaginatedResponse, summary="Obtener clientes", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, ENTRENADOR]))])
def read_clientes(
    cedula_filtro: Optional[str] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return cliente_service.obtener_clientes_paginados(db=db, page=page, page_size=page_size, cedula=cedula_filtro)

@router.patch("/{id_cliente}", response_model=cliente_schema.ClienteResponse, summary="Actualizar cliente", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def update_cliente(*, db: Session = Depends(get_db), id_cliente: int, cliente_in: cliente_schema.ClienteUpdate):
    return cliente_service.actualizar_cliente(db=db, id_cliente=id_cliente, cliente_in=cliente_in)