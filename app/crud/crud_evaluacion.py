from app.crud.base import CRUDBase
from app.models.evaluacion_biometrica import EvaluacionBiometrica

class CRUDEvaluacionBiometrica(CRUDBase[EvaluacionBiometrica]):
    # Si luego necesitas obtener el historial de un solo cliente, 
    # puedes agregar un método aquí: get_by_cliente(self, db, id_cliente)
    pass

# Instanciamos la clase para exportarla
evaluacion = CRUDEvaluacionBiometrica(EvaluacionBiometrica)