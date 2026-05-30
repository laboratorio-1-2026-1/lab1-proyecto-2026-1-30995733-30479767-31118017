from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.base import CRUDBase
from app.models.usuario_model import Usuario
from app.core.security import get_password_hash

class CRUDUsuario(CRUDBase[Usuario]):

    def create_user(self, db: Session, *, obj_in: dict) -> Usuario:

        password_plana = obj_in.pop("password")

        hashed_password = get_password_hash(password_plana)

        obj_in["password"] = hashed_password

        return super().create(db, obj_in=obj_in)

    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        return db.query(self.model).filter(self.model.email == email).first()

    def obtener_query_filtrada(self, db: Session, email_filtro: Optional[str] = None, id_rol: Optional[int] = None):

        query = db.query(self.model)
        if email_filtro:
            query = query.filter(self.model.email.ilike(f"%{email_filtro}%"))
        if id_rol:
            query = query.filter(self.model.id_rol == id_rol)
        return query

usuario = CRUDUsuario(Usuario)