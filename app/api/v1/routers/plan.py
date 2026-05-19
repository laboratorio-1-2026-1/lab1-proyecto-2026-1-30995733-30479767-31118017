from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_current_user 
from app.models.usuario import Usuario
from app.schemas import plan_schema
from app.crud.crud_plan import plan as crud_plan
from app.db.database import get_db 

router = APIRouter()

@router.post("/", response_model=plan_schema.PlanResponse)
def create_plan(
    *,
    db: Session = Depends(get_db),
    plan_in: plan_schema.PlanCreate
):

    if plan_in.precio_sub <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio del plan debe ser mayor a cero."
            )
    if plan_in.duracion_dias <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración del plan debe ser de al menos 1 día.")

    nuevo_plan = crud_plan.create(db, obj_in=plan_in.model_dump())
    return nuevo_plan

@router.get("/", response_model=List[plan_schema.PlanResponse])
def read_planes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):

    planes = crud_plan.get_multi(db, skip=skip, limit=limit)
    return planes

@router.put("/{id_plan}", response_model=plan_schema.PlanResponse)
def update_plan(
    *,
    db: Session = Depends(get_db),
    id_plan: int,
    plan_in: plan_schema.PlanUpdate,
    current_user: Usuario = Depends(get_current_user)
):

    plan_actual = crud_plan.get(db=db, id=id_plan)
    if not plan_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error: No se encontró ningún plan con el ID {id_plan}"
        )

    if plan_in.precio_sub is not None and plan_in.precio_sub <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio del plan debe ser estrictamente mayor a cero."
        )
        
    if plan_in.duracion_dias is not None and plan_in.duracion_dias <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración del plan debe ser de al menos 1 día."
        )

    plan_actualizado = crud_plan.update(db=db, db_obj=plan_actual, obj_in=plan_in)
    
    return plan_actualizado