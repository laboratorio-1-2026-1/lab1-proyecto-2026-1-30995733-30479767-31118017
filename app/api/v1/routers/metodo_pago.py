from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import metodo_pago_schema
from app.db.database import get_db
from app.services import metodo_pago_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, CLIENTE, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=metodo_pago_schema.MetodoPagoResponse, summary="Crear método de pago", status_code=status.HTTP_201_CREATED, dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_metodo_pago(*, db: Session = Depends(get_db), metodo_in: metodo_pago_schema.MetodoPagoCreate):
    return metodo_pago_service.crear_metodo_pago(db=db, metodo_in=metodo_in)

@router.get("/", response_model=metodo_pago_schema.MetodoPagoPaginatedResponse, summary="Obtener métodos de pago", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, CLIENTE, ENTRENADOR]))])
def read_metodos_pago(
    nombre_metodo: Optional[str] = Query(None, description="Filtrar por nombre de método (ej: Efectivo)"), 
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return metodo_pago_service.obtener_metodos_pago_paginados(db=db, page=page, page_size=page_size, nombre_metodo=nombre_metodo)

@router.patch("/{id_metodo}", response_model=metodo_pago_schema.MetodoPagoResponse, summary="Actualizar método de pago", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def update_metodo_pago(*, db: Session = Depends(get_db), id_metodo: int, metodo_in: metodo_pago_schema.MetodoPagoUpdate):
    return metodo_pago_service.actualizar_metodo_pago(db=db, id_metodo=id_metodo, metodo_in=metodo_in)