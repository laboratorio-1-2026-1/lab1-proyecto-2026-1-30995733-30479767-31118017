from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario
from app.schemas import control_acceso_schema
from app.crud.crud_control_acceso import control_acceso as crud_control_acceso
from app.crud.crud_cliente import cliente as crud_cliente 
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=control_acceso_schema.ControlAccesoResponse)
def create_acceso(
    *,
    db: Session = Depends(get_db),
    acceso_in: control_acceso_schema.ControlAccesoCreate,
    current_user: Usuario = Depends(get_current_user)
):
    cliente_db = crud_cliente.get(db=db, id=acceso_in.id_cliente)
    if not cliente_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: El cliente ingresado no existe en el sistema.")

    nuevo_acceso = crud_control_acceso.create(db=db, obj_in=acceso_in.model_dump())
    return nuevo_acceso

@router.get("/", response_model=control_acceso_schema.ControlAccesoPaginatedResponse)
def read_accesos(
    db: Session = Depends(get_db), 
    page: int = 1, 
    page_size: int = 10,
    current_user: Usuario = Depends(get_current_user)
):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_control_acceso.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    accesos = crud_control_acceso.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": accesos
    }