from typing import Any, Dict, Union, Optional
from sqlalchemy.orm import Session
from app.repositories.base import CRUDBase
from app.models.ticket_mantenimiento_model import TicketMantenimiento
from app.schemas.ticket_mantenimiento_schema import TicketMantenimientoUpdate

class CRUDTicketMantenimiento(CRUDBase[TicketMantenimiento]):
    
    def obtener_query_filtrada(self, db: Session, id_maquina: Optional[int] = None):

        query = db.query(self.model)
        
        if id_maquina is not None:
            query = query.filter(self.model.id_maquina == id_maquina)
            
        return query.order_by(self.model.fecha_falla.desc())

    def update(
        self, 
        db: Session, 
        *, 
        db_obj: TicketMantenimiento, 
        obj_in: Union[TicketMantenimientoUpdate, Dict[str, Any]]
    ) -> TicketMantenimiento:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

ticket_mantenimiento = CRUDTicketMantenimiento(TicketMantenimiento)