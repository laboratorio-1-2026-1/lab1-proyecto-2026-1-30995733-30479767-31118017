from sqlalchemy.orm import Session
from datetime import datetime
from app.core.security import get_password_hash
from app.models.rol_model import Rol
from app.models.usuario_model import Usuario
from app.models.cliente_model import Cliente
from app.models.entrenador_model import Entrenador
from app.models.disciplina_model import Disciplina
from app.models.categoria_maquina_model import CategoriaMaquina
from app.models.maquina_model import Maquina
from app.models.plan_subscripcion_model import PlanSubscripcion
from app.models.producto_model import Producto
from app.models.metodo_pago_model import MetodoPago
from app.models.pago_membresia_model import PagoMembresia
from app.models.membresia_model import Membresia

def poblar_datos_semilla(db: Session):
    if db.query(Rol).first():
        print("Los datos de prueba ya existen. Saltando inicialización.")
        return

    print("Iniciando inyección masiva y estricta de datos de prueba...")

    rol_admin = Rol(id_rol=1, nombre_rol="Administrador", descripcion="Control total del sistema")
    rol_finanzas = Rol(id_rol=2, nombre_rol="Finanzas", descripcion="Gestión de pagos")
    rol_entrenador = Rol(id_rol=3, nombre_rol="Entrenador", descripcion="Staff deportivo")
    rol_cliente = Rol(id_rol=4, nombre_rol="Cliente", descripcion="Usuario regular")
    db.add_all([rol_admin, rol_finanzas, rol_entrenador, rol_cliente])
    db.flush() 

    plan_mensual = PlanSubscripcion(nombre_plan="Plan Mensual Base", precio_sub=30.0, duracion_dias=30, descripcion="Acceso por un mes")
    plan_trimestral = PlanSubscripcion(nombre_plan="Plan Trimestral Pro", precio_sub=80.0, duracion_dias=90, descripcion="Acceso por tres meses")
    plan_anual = PlanSubscripcion(nombre_plan="Plan Anual VIP", precio_sub=300.0, duracion_dias=365, descripcion="Acceso anual completo")
    db.add_all([plan_mensual, plan_trimestral, plan_anual])

    mp_efectivo = MetodoPago(nombre_metodo="Efectivo")
    mp_zelle = MetodoPago(nombre_metodo="Zelle")
    mp_tdc = MetodoPago(nombre_metodo="Tarjeta De Credito")
    db.add_all([mp_efectivo, mp_zelle, mp_tdc])
    db.flush()

    pwd_hash = get_password_hash("123456789") # Contraseña universal
    
    u_admin = Usuario(id_rol=1, email="admin@smartgym.com", password=pwd_hash)
    u_finanzas = Usuario(id_rol=2, email="finanzas@smartgym.com", password=pwd_hash)

    u_ent1 = Usuario(id_rol=3, email="carlos.ent@smartgym.com", password=pwd_hash)
    u_ent2 = Usuario(id_rol=3, email="maria.ent@smartgym.com", password=pwd_hash)
    u_ent3 = Usuario(id_rol=3, email="jose.ent@smartgym.com", password=pwd_hash)

    u_cli1 = Usuario(id_rol=4, email="ana.cliente@gmail.com", password=pwd_hash)
    u_cli2 = Usuario(id_rol=4, email="luis.cliente@gmail.com", password=pwd_hash)
    u_cli3 = Usuario(id_rol=4, email="sofia.cliente@gmail.com", password=pwd_hash)
    u_cli4 = Usuario(id_rol=4, email="miguel.cliente@gmail.com", password=pwd_hash)
    u_cli5 = Usuario(id_rol=4, email="lucia.cliente@gmail.com", password=pwd_hash)

    db.add_all([u_admin, u_finanzas, u_ent1, u_ent2, u_ent3, u_cli1, u_cli2, u_cli3, u_cli4, u_cli5])
    db.flush()


    ent1 = Entrenador(id_usuario=u_ent1.id_user, nombre_ent="Carlos", apellido_ent="Gomez", especialidad="CrossFit")
    ent2 = Entrenador(id_usuario=u_ent2.id_user, nombre_ent="Maria", apellido_ent="Perez", especialidad="Yoga")
    ent3 = Entrenador(id_usuario=u_ent3.id_user, nombre_ent="Jose", apellido_ent="Ruiz", especialidad="Pesas")
    db.add_all([ent1, ent2, ent3])


    cli1 = Cliente(id_usuario=u_cli1.id_user, nombre_cli="Ana", apellido_cli="Lopez", cedula="V-11111111")
    cli2 = Cliente(id_usuario=u_cli2.id_user, nombre_cli="Luis", apellido_cli="Martinez", cedula="V-22222222")
    cli3 = Cliente(id_usuario=u_cli3.id_user, nombre_cli="Sofia", apellido_cli="Fernandez", cedula="V-33333333")
    cli4 = Cliente(id_usuario=u_cli4.id_user, nombre_cli="Miguel", apellido_cli="Torres", cedula="V-44444444")
    cli5 = Cliente(id_usuario=u_cli5.id_user, nombre_cli="Lucia", apellido_cli="Diaz", cedula="V-55555555")
    db.add_all([cli1, cli2, cli3, cli4, cli5])
    db.flush()


    pago1 = PagoMembresia(id_cliente=cli1.id_cliente, id_metodo=mp_zelle.id_metodo, monto_membresia=300.0, referencia="ZELLE-ACT-01", fecha_pago=datetime(2026, 1, 15, 10, 0))
    db.add(pago1)
    db.flush()
    mem1 = Membresia(id_cliente=cli1.id_cliente, id_plan=plan_anual.id_plan, id_pago=pago1.id_pago, fecha_inicio=datetime(2026, 1, 15), fecha_fin=datetime(2026, 9, 15), estado=True)
    pago2 = PagoMembresia(id_cliente=cli2.id_cliente, id_metodo=mp_efectivo.id_metodo, monto_membresia=30.0, referencia="CASH-VEN-02", fecha_pago=datetime(2025, 8, 1, 9, 30))
    db.add(pago2)
    db.flush()
    mem2 = Membresia(id_cliente=cli2.id_cliente, id_plan=plan_mensual.id_plan, id_pago=pago2.id_pago, fecha_inicio=datetime(2025, 8, 1), fecha_fin=datetime(2025, 9, 1), estado=True) 
    pago3 = PagoMembresia(id_cliente=cli3.id_cliente, id_metodo=mp_tdc.id_metodo, monto_membresia=30.0, referencia="TDC-PRX-03", fecha_pago=datetime(2026, 4, 29, 14, 0))
    db.add(pago3)
    db.flush()
    mem3 = Membresia(id_cliente=cli3.id_cliente, id_plan=plan_mensual.id_plan, id_pago=pago3.id_pago, fecha_inicio=datetime(2026, 4, 29), fecha_fin=datetime(2026, 5, 29), estado=True)
    pago4 = PagoMembresia(id_cliente=cli4.id_cliente, id_metodo=mp_tdc.id_metodo, monto_membresia=80.0, referencia="TDC-SUS-04", fecha_pago=datetime(2026, 5, 1, 11, 0))
    db.add(pago4)
    db.flush()
    mem4 = Membresia(id_cliente=cli4.id_cliente, id_plan=plan_trimestral.id_plan, id_pago=pago4.id_pago, fecha_inicio=datetime(2026, 5, 1), fecha_fin=datetime(2026, 8, 1), estado=False) 
    pago5 = PagoMembresia(id_cliente=cli5.id_cliente, id_metodo=mp_zelle.id_metodo, monto_membresia=30.0, referencia="ZELLE-AGO-05", fecha_pago=datetime(2026, 8, 10, 16, 45))
    db.add(pago5)
    db.flush()
    mem5 = Membresia(id_cliente=cli5.id_cliente, id_plan=plan_mensual.id_plan, id_pago=pago5.id_pago, fecha_inicio=datetime(2026, 8, 10), fecha_fin=datetime(2026, 9, 10), estado=True)
    db.add_all([mem1, mem2, mem3, mem4, mem5])


    cat_cardio = CategoriaMaquina(nombre_categoria="Cardio")
    cat_fuerza = CategoriaMaquina(nombre_categoria="Fuerza")
    cat_libres = CategoriaMaquina(nombre_categoria="Pesos Libres")
    db.add_all([cat_cardio, cat_fuerza, cat_libres])
    db.flush()

    maq1 = Maquina(
        id_categoria=cat_cardio.id_categoria, 
        nombre="Caminadora Pro X", 
        descripcion_tecnica="Motor de 4HP, inclinación hasta 15% y pantalla LED táctil.", 
        estado_maquina="Operativa"
    )
    maq2 = Maquina(
        id_categoria=cat_cardio.id_categoria, 
        nombre="Bicicleta de Spinning", 
        descripcion_tecnica="Volante de inercia de 20kg con resistencia magnética ajustable.", 
        estado_maquina="En Mantenimiento"
    )
    maq3 = Maquina(
        id_categoria=cat_fuerza.id_categoria, 
        nombre="Prensa de Piernas 45", 
        descripcion_tecnica="Estructura de acero reforzado, soporta hasta 400kg en discos.", 
        estado_maquina="Operativa"
    )
    maq4 = Maquina(
        id_categoria=cat_fuerza.id_categoria, 
        nombre="Extensión de Cuádriceps", 
        descripcion_tecnica="Torre de pesas de 100kg con poleas de tracción suave.", 
        estado_maquina="Fuera de Servicio"
    )
    maq5 = Maquina(
        id_categoria=cat_libres.id_categoria, 
        nombre="Banco Plano Olímpico", 
        descripcion_tecnica="Tapizado de alta densidad anti-sudor y soportes cromados.", 
        estado_maquina="Operativa"
    )
    db.add_all([maq1, maq2, maq3, maq4, maq5])


    disc1 = Disciplina(nombre_disc="Yoga", descripcion="Clases de flexibilidad.")
    disc2 = Disciplina(nombre_disc="CrossFit", descripcion="Alta intensidad.")
    disc3 = Disciplina(nombre_disc="Pilates", descripcion="Fortalecimiento core.")
    db.add_all([disc1, disc2, disc3])

    prod1 = Producto(nombre_prod="Proteína Whey 2lbs", precio=45.0, stock=20)
    prod2 = Producto(nombre_prod="Creatina Monohidratada", precio=25.0, stock=15)
    prod3 = Producto(nombre_prod="Agua Mineral 500ml", precio=1.5, stock=100)
    db.add_all([prod1, prod2, prod3])

    db.commit()
    print("¡Base de datos abombada exitosamente con mapeo estricto de roles!")