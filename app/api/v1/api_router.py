from fastapi import APIRouter
from app.api.v1.routers import (
    auth, rol, usuario,
    categoria_maquina, maquina, ticket_mantenimiento,
    disciplina, entrenador, sesion,
    cliente, reserva,
    control_acceso,
    plan, metodo_pago, pago_membresia, membresia,
    evaluacion_biometrica,
    producto, venta_producto, registro_venta
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["2.1 Seguridad y Usuarios"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["2.1 Seguridad y Usuarios"])
api_router.include_router(rol.router, prefix="/roles", tags=["2.1 Seguridad y Usuarios"])

api_router.include_router(categoria_maquina.router, prefix="/categorias-maquina", tags=["2.2 Inventario de Máquinas"])
api_router.include_router(maquina.router, prefix="/maquinas", tags=["2.2 Inventario de Máquinas"])

api_router.include_router(disciplina.router, prefix="/disciplinas", tags=["2.3 Gestión Deportiva"])
api_router.include_router(entrenador.router, prefix="/entrenadores", tags=["2.3 Gestión Deportiva"])
api_router.include_router(sesion.router, prefix="/sesiones-clase", tags=["2.3 Gestión Deportiva"])

api_router.include_router(cliente.router, prefix="/clientes", tags=["2.4 Clientes y Reservas"])
api_router.include_router(reserva.router, prefix="/reservas", tags=["2.4 Clientes y Reservas"])

api_router.include_router(control_acceso.router, prefix="/control-acceso", tags=["2.5 Control de Acceso Físico"])

api_router.include_router(plan.router, prefix="/planes", tags=["2.6 Finanzas y Suscripciones"])
api_router.include_router(metodo_pago.router, prefix="/metodos-pago", tags=["2.6 Finanzas y Suscripciones"])
api_router.include_router(pago_membresia.router, prefix="/pagos-membresia", tags=["2.6 Finanzas y Suscripciones"])
api_router.include_router(membresia.router, prefix="/membresias", tags=["2.6 Finanzas y Suscripciones"])

api_router.include_router(evaluacion_biometrica.router, prefix="/evaluaciones", tags=["2.7 Seguimiento Biométrico"])

api_router.include_router(producto.router, prefix="/productos", tags=["2.8 Tienda POS"])
api_router.include_router(registro_venta.router, prefix="/registros-venta", tags=["2.8 Tienda POS"])
api_router.include_router(venta_producto.router, prefix="/ventas", tags=["2.8 Tienda POS"])


api_router.include_router(ticket_mantenimiento.router, prefix="/tickets-mantenimiento", tags=["2.9 Mantenimiento"])