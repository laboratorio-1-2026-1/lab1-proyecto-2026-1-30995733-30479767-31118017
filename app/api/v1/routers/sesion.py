from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
import math
from typing import List
from app.schemas import sesion_clase_schema
from app.crud.crud_sesion import sesion as crud_sesion
from app.models.sesion_clase import SesionClase
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=sesion_clase_schema.SesionClaseResponse)
def create_sesion(
    *,
    db: Session = Depends(get_db),
    sesion_in: sesion_clase_schema.SesionClaseCreate
):

    inicio_real = sesion_in.fecha_inic.replace(tzinfo=None)
    fin_real = sesion_in.fecha_fin.replace(tzinfo=None)

# Validaciones para evitar choques de horarios y datos incorrectos
    if inicio_real >= fin_real:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio debe ser anterior a la de finalización."
        )
    if sesion_in.cupos < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de cupos asignados no puede ser negativo."
        )

    clase_chocante = db.query(SesionClase).filter(
        and_(
            SesionClase.id_entrenador == sesion_in.id_entrenador,
            inicio_real < SesionClase.fecha_fin,
            fin_real > SesionClase.fecha_inic
        )
    ).first()

    if clase_chocante:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Conflicto Horario: El entrenador ya tiene una clase asignada de {clase_chocante.fecha_inic.strftime('%H:%M')} a {clase_chocante.fecha_fin.strftime('%H:%M')}."
        )

    datos_guardar = sesion_in.model_dump()
    datos_guardar["fecha_inic"] = inicio_real
    datos_guardar["fecha_fin"] = fin_real

    nueva_sesion = crud_sesion.create(db, obj_in=datos_guardar)
    return nueva_sesion


@router.get("/", response_model=sesion_clase_schema.SesionClasePaginatedResponse)
def read_sesiones(db: Session = Depends(get_db), page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Los parámetros de página deben ser mayores a 0.")
    
    total_rows = db.query(crud_sesion.model).count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    
    skip = (page - 1) * page_size
    sesiones = crud_sesion.get_multi(db, skip=skip, limit=page_size)
    
    return {
        "meta": {"total_rows": total_rows, "current_page": page, "page_size": page_size, "total_pages": total_pages},
        "rows": sesiones
    }