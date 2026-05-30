from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import control_acceso_schema
from app.db.database import get_db
from app.services import control_acceso_service
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=control_acceso_schema.ControlAccesoResponse, dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, ENTRENADOR]))])
def registrar_entrada(
    *,
    db: Session = Depends(get_db),
    torniquete_in: control_acceso_schema.TorniqueteInput
):
    return control_acceso_service.procesar_entrada_torniquete(db=db, torniquete_in=torniquete_in)

@router.get("/", response_model=control_acceso_schema.ControlAccesoPaginatedResponse, dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def consultar_bitacora(
    cedula: Optional[str] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return control_acceso_service.obtener_accesos_paginados(db=db, page=page, page_size=page_size, cedula=cedula)