from app.crud.base import CRUDBase
from app.models.plan_subscripcion import PlanSubscripcion 

class CRUDPlan(CRUDBase[PlanSubscripcion]):
    pass

plan = CRUDPlan(PlanSubscripcion)