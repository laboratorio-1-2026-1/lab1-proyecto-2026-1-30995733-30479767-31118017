from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math
from app.schemas import membresia_schema
from app.crud.crud_membresia import membresia as crud_membresia
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=membresia_schema.MembresiaResponse, status_code=status.HTTP_201_CREATED)
def create_membresia(
    *,
    db: Session = Depends(get_db),
    membresia_in: membresia_schema.MembresiaCreate
):
    if membresia_in.fecha_fin <= membresia_in.fecha_inicio:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha de finalización debe ser posterior a la de inicio.")
    
    obj_data = membresia_in.model_dump()
    if isinstance(obj_data.get("estado"), str):
        obj_data["estado"] = obj_data["estado"].lower() in ["activa", "activo", "true", "1"]
    
    nueva_membresia = crud_membresia.create(db, obj_in=obj_data)
    nueva_membresia.estado = "Activa" if nueva_membresia.estado else "Inactiva"
    return nueva_membresia

@router.get("/", response_model=membresia_schema.MembresiaPaginatedResponse)
def read_membresias(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_membresia.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    membresias = crud_membresia.get_multi(db, skip=skip, limit=page_size)
    
    for m in membresias:
        m.estado = "Activa" if m.estado else "Inactiva"
        
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": membresias
    }

@router.get("/{id_membresia}", response_model=membresia_schema.MembresiaResponse)
def read_membresia_by_id(id_membresia: int, db: Session = Depends(get_db)):
    membresia = crud_membresia.get(db, id=id_membresia)
    if not membresia:
         raise HTTPException(status_code=404, detail="Membresía no encontrada.")
    membresia.estado = "Activa" if membresia.estado else "Inactiva"
    return membresia