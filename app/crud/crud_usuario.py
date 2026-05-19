from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.usuario import Usuario
from app.core.security import get_password_hash

class CRUDUsuario(CRUDBase[Usuario]):

    def create_user(self, db: Session, *, obj_in: dict) -> Usuario:
        # 1. Extraemos y separamos la clave plana del diccionario usando pop()
        # Esto asegura que aislemos solo el texto de la contraseña.
        password_plana = obj_in.pop("password")

        # 2. Encriptamos la contraseña sola
        hashed_password = get_password_hash(password_plana)

        # 3. Volvemos a inyectar la clave (ahora encriptada) en el diccionario
        obj_in["password"] = hashed_password

        # 4. Llamamos a la clase padre (CRUDBase) para que haga el insert en PostgreSQL
        return super().create(db, obj_in=obj_in)

    def get_by_email(self, db: Session, email: str) -> Usuario:
        return db.query(self.model).filter(self.model.email == email).first()

# Instanciamos la clase para que tu endpoint la pueda importar como "crud_usuario"
usuario = CRUDUsuario(Usuario)