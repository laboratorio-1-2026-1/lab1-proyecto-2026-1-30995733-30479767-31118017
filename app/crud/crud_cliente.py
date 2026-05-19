from app.crud.base import CRUDBase
from app.models.cliente import Cliente

class CRUDCliente(CRUDBase[Cliente]):
    # Aquí puedes añadir métodos personalizados a futuro si necesitas
    # buscar clientes por DNI, teléfono, etc.
    pass

# Instanciamos la clase para exportarla
cliente = CRUDCliente(Cliente)