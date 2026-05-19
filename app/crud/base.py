from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Any)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.get(self.model, id)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, 
            db: Session, 
            *, 
            db_obj: ModelType, 
            obj_in: Any
        ) -> ModelType:
            # 1. Convertimos el objeto actual de la base de datos a un diccionario
            obj_data = jsonable_encoder(db_obj)

            # 2. Verificamos si los datos nuevos vienen como diccionario o como un Schema Pydantic
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                # exclude_unset=True es clave para los PATCH, solo toma lo que el usuario envió
                update_data = obj_in.model_dump(exclude_unset=True)

            # 3. Comparamos y reemplazamos solo los campos que cambiaron
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            # 4. Guardamos los cambios en PostgreSQL
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj