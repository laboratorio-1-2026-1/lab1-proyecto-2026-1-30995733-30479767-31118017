from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import plan_schema
from app.db.database import get_db 
from app.services import plan_service 
from app.api.dependencies import VerificarRol, ADMIN, FINANZAS, CLIENTE, ENTRENADOR

router = APIRouter()

@router.post("/", response_model=plan_schema.PlanResponse, summary="Crear plan", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def create_plan(*, db: Session = Depends(get_db), plan_in: plan_schema.PlanCreate):
    return plan_service.crear_plan(db=db, plan_in=plan_in)

@router.get("/", response_model=plan_schema.PlanPaginatedResponse, summary="Obtener planes", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS, ENTRENADOR, CLIENTE]))])
def read_planes(
    nombre_plan: Optional[str] = None,
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    return plan_service.obtener_planes_paginados(db=db, page=page, page_size=page_size, nombre=nombre_plan)

@router.patch("/{id_plan}", response_model=plan_schema.PlanResponse, summary="Actualizar plan", dependencies=[Depends(VerificarRol([ADMIN, FINANZAS]))])
def update_plan(*, db: Session = Depends(get_db), id_plan: int, plan_in: plan_schema.PlanUpdate):
    return plan_service.actualizar_plan(db=db, id_plan=id_plan, plan_in=plan_in)