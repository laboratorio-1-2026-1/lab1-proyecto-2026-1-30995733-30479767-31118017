from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.plan_subscripcion_model import PlanSubscripcion 

class CRUDPlan(CRUDBase[PlanSubscripcion]):
    
    def obtener_query_filtrada(self, db: Session, nombre_plan: Optional[str] = None):

        query = db.query(self.model)
        if nombre_plan:
            query = query.filter(self.model.nombre_plan.ilike(f"%{nombre_plan}%"))
        return query

    def get_by_nombre(self, db: Session, nombre_plan: str) -> Optional[PlanSubscripcion]:
        return db.query(self.model).filter(func.lower(self.model.nombre_plan) == func.lower(nombre_plan)).first()

plan = CRUDPlan(PlanSubscripcion)