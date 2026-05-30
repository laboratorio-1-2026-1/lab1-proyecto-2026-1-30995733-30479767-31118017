from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import registro_venta_schema
from app.db.database import get_db
from app.services import registro_venta_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS

router = APIRouter()

@router.post("/", response_model=registro_venta_schema.RegistroVentaResponse, summary="Crear registro de venta", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_registro_venta(*, db: Session = Depends(get_db), registro_in: registro_venta_schema.RegistroVentaCreate):
    return registro_venta_service.crear_registro_venta(db=db, registro_in=registro_in)

@router.get("/", response_model=registro_venta_schema.RegistroVentaPaginatedResponse, summary="Obtener registros de venta", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def read_registros_venta(
    id_producto: Optional[int] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return registro_venta_service.obtener_registros_paginados(db=db, page=page, page_size=page_size, id_producto=id_producto)