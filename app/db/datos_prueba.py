from sqlalchemy.orm import Session
from app.core.security import get_password_hash


from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.categoria_maquina import CategoriaMaquina
from app.models.maquina import Maquina
from app.models.plan_subscripcion import PlanSubscripcion
from app.models.producto import Producto

def poblar_datos_semilla(db: Session):
    # Condición de seguridad: Comprobar si ya existen roles. 
    # Si ya hay datos, detenemos el script para no duplicarlos cada vez que inicie el servidor.
    if db.query(Rol).first():
        print("Los datos de prueba ya existen. Saltando inicialización.")
        return

    print("Creando datos de prueba...")

    # Los Roles fundamentales (Administración, Finanzas, Entrenadores y Clientes)
    rol_admin = Rol(nombre_rol="Administración", descripcion="Control total del sistema")
    rol_finanzas = Rol(nombre_rol="Finanzas", descripcion="Gestión de pagos y suscripciones")
    rol_entrenador = Rol(nombre_rol="Entrenador", descripcion="Gestión de clases y evaluaciones")
    rol_cliente = Rol(nombre_rol="Cliente", descripcion="Usuario regular del gimnasio")
    db.add_all([rol_admin, rol_finanzas, rol_entrenador, rol_cliente])
    db.commit()

    # 2. 1 Usuario Administrador [cite: 119]
    usuario_admin = Usuario(
        email="admin@smartgym.com",
        password=get_password_hash("1234"), 
        id_rol=rol_admin.id_rol
    )
    db.add(usuario_admin)
    db.commit()

    # 3 Categorías de máquinas
    cat_cardio = CategoriaMaquina(nombre_categoria="Cardiovascular")
    cat_musculacion = CategoriaMaquina(nombre_categoria="Musculación")
    cat_peso_libre = CategoriaMaquina(nombre_categoria="Peso Libre")
    db.add_all([cat_cardio, cat_musculacion, cat_peso_libre])
    db.commit()

    # 5 máquinas de ejemplo
    maq1 = Maquina(nombre="Caminadora", id_categoria=cat_cardio.id_categoria)
    maq2 = Maquina(nombre="Bicicleta Estática", id_categoria=cat_cardio.id_categoria)
    maq3 = Maquina(nombre="Prensa de Piernas", id_categoria=cat_musculacion.id_categoria)
    maq4 = Maquina(nombre="Máquina de Poleas", id_categoria=cat_musculacion.id_categoria)
    maq5 = Maquina(nombre="Banco Plano", id_categoria=cat_peso_libre.id_categoria)
    db.add_all([maq1, maq2, maq3, maq4, maq5])
    db.commit()

    # 2 Planes de suscripción
    plan_basico = PlanSubscripcion(nombre_plan="Plan Básico", precio_sub=20.0, duracion_dias=30, descripcion="Para pobres")
    plan_vip = PlanSubscripcion(nombre_plan="Plan VIP", precio_sub=50.0, duracion_dias=30, descripcion="Para Fresas")
    db.add_all([plan_basico, plan_vip])
    db.commit()

    # 3 Productos en la tienda
    prod1 = Producto(nombre_prod="Botella de Agua", precio=1.5, stock=100) 
    prod2 = Producto(nombre_prod="Proteína 1kg", precio=35.0, stock=20)
    prod3 = Producto(nombre_prod="Toalla Deportiva", precio=5.0, stock=50)
    
    db.add_all([prod1, prod2, prod3])
    db.commit()