from app.crud.base import CRUDBase
from app.models.disciplina import Disciplina

class CRUDDisciplina(CRUDBase[Disciplina]):
    pass

disciplina = CRUDDisciplina(Disciplina)