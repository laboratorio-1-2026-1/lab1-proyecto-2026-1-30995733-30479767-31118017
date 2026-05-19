from sqlalchemy.orm import Session
from app.core.security import get_password_hash

from app.models.disciplina import Disciplina
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

    # 2. 1 Usuario Administrador
    usuario_admin = Usuario(
        email="admin@smartgym.com",
        password=get_password_hash("1234"), 
        id_rol=rol_admin.id_rol
    )
    db.add(usuario_admin)
    db.commit()

    # 15 Categorías de máquinas
    cat_cardio = CategoriaMaquina(nombre_categoria="Cardiovascular")
    cat_musculacion = CategoriaMaquina(nombre_categoria="Musculación")
    cat_peso_libre = CategoriaMaquina(nombre_categoria="Peso Libre")
    cat_funcional = CategoriaMaquina(nombre_categoria="Entrenamiento Funcional")
    cat_crossfit = CategoriaMaquina(nombre_categoria="Crossfit")
    cat_pilates = CategoriaMaquina(nombre_categoria="Pilates")
    cat_yoga = CategoriaMaquina(nombre_categoria="Yoga")
    cat_rehab = CategoriaMaquina(nombre_categoria="Rehabilitación")
    cat_abdomen = CategoriaMaquina(nombre_categoria="Abdomen y Core")
    cat_flex = CategoriaMaquina(nombre_categoria="Flexibilidad y Estiramiento")
    cat_remo = CategoriaMaquina(nombre_categoria="Remo Indoor")
    cat_spinning = CategoriaMaquina(nombre_categoria="Spinning")
    cat_calistenia = CategoriaMaquina(nombre_categoria="Calistenia")
    cat_trx = CategoriaMaquina(nombre_categoria="Suspensión TRX")
    cat_olimpico = CategoriaMaquina(nombre_categoria="Halterofilia")

    db.add_all([
        cat_cardio, cat_musculacion, cat_peso_libre, cat_funcional, cat_crossfit,
        cat_pilates, cat_yoga, cat_rehab, cat_abdomen, cat_flex,
        cat_remo, cat_spinning, cat_calistenia, cat_trx, cat_olimpico
    ])
    db.commit()


    # 20 máquinas de ejemplo
    maq1 = Maquina(nombre="Caminadora", id_categoria=cat_cardio.id_categoria)
    maq2 = Maquina(nombre="Bicicleta Estática", id_categoria=cat_cardio.id_categoria)
    maq3 = Maquina(nombre="Prensa de Piernas", id_categoria=cat_musculacion.id_categoria)
    maq4 = Maquina(nombre="Máquina de Poleas", id_categoria=cat_musculacion.id_categoria)
    maq5 = Maquina(nombre="Banco Plano", id_categoria=cat_peso_libre.id_categoria)
    maq6 = Maquina(nombre="Elíptica Magnética", id_categoria=cat_cardio.id_categoria)
    maq7 = Maquina(nombre="Escaladora Infinita (StairMaster)", id_categoria=cat_cardio.id_categoria)
    maq8 = Maquina(nombre="Remoergómetro Concept2", id_categoria=cat_remo.id_categoria)
    maq9 = Maquina(nombre="Bicicleta de Spinning", id_categoria=cat_spinning.id_categoria)
    maq10 = Maquina(nombre="Banco Inclinado", id_categoria=cat_peso_libre.id_categoria)
    maq11 = Maquina(nombre="Banco Declinado", id_categoria=cat_peso_libre.id_categoria)
    maq12 = Maquina(nombre="Máquina Extensión de Cuádriceps", id_categoria=cat_musculacion.id_categoria)
    maq13 = Maquina(nombre="Máquina Curl Femoral Tumbado", id_categoria=cat_musculacion.id_categoria)
    maq14 = Maquina(nombre="Multipower / Smith Machine", id_categoria=cat_musculacion.id_categoria)
    maq15 = Maquina(nombre="Silla Romana", id_categoria=cat_abdomen.id_categoria)
    maq16 = Maquina(nombre="Máquina Crunch Abdominal", id_categoria=cat_abdomen.id_categoria)
    maq17 = Maquina(nombre="Jaula de Crossfit (Rig)", id_categoria=cat_crossfit.id_categoria)
    maq18 = Maquina(nombre="Cajas Pliométricas (Plyo Boxes)", id_categoria=cat_funcional.id_categoria)
    maq19 = Maquina(nombre="Cama Reformer", id_categoria=cat_pilates.id_categoria)
    maq20 = Maquina(nombre="Bandas de Suspensión TRX", id_categoria=cat_trx.id_categoria)

    db.add_all([
        maq1, maq2, maq3, maq4, maq5, maq6, maq7, maq8, maq9, maq10,
        maq11, maq12, maq13, maq14, maq15, maq16, maq17, maq18, maq19, maq20
    ])
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

    prod4 = Producto(nombre_prod="Pepsi", precio=5.0, stock=50)
    prod5 = Producto(nombre_prod="Coca-Cola", precio=25.0, stock=50)
    prod6 = Producto(nombre_prod="RedBull", precio=15.0, stock=50)
    prod7 = Producto(nombre_prod="Jugo de naranja", precio=75.0, stock=50)
    prod8 = Producto(nombre_prod="Limonada", precio=5.0, stock=50)
    prod9 = Producto(nombre_prod="Guantes", precio=5.0, stock=50)
    prod10 = Producto(nombre_prod="Camisa Deportiva", precio=5.0, stock=50)
    prod11 = Producto(nombre_prod="Short Deportivo", precio=5.0, stock=50)
    prod12 = Producto(nombre_prod="Zapatos Deportivos", precio=5.0, stock=50)
    prod13 = Producto(nombre_prod="Audifonos", precio=5.0, stock=50)
    prod14 = Producto(nombre_prod="Savoy", precio=5.0, stock=50)
    prod15 = Producto(nombre_prod="Manzanas", precio=5.0, stock=50)
    prod16 = Producto(nombre_prod="Mandarina", precio=5.0, stock=50)
    prod17 = Producto(nombre_prod="Cocossete", precio=5.0, stock=50)
    prod18 = Producto(nombre_prod="Muñequera", precio=5.0, stock=50)
    prod19 = Producto(nombre_prod="Rodillera", precio=5.0, stock=50)
    prod20 = Producto(nombre_prod="Creatina", precio=5.0, stock=50)

    db.add_all([prod1, prod2, prod3,prod4,prod5,prod6,prod7,prod8,prod9,prod10,prod11,prod12,prod13,prod14,prod15,prod16,prod17,prod18,
                prod19,prod20,])
    db.commit()





    #Disciplinas

    disc1 = Disciplina(nombre_disc="Yoga", descripcion="Clase de relajación, respiración y flexibilidad.")
    disc2 = Disciplina(nombre_disc="Crossfit", descripcion="Entrenamiento funcional de alta intensidad (WOD).")
    disc3 = Disciplina(nombre_disc="Pilates Reformer", descripcion="Ejercicios de bajo impacto para el core y la postura.")
    disc4 = Disciplina(nombre_disc="Spinning", descripcion="Ciclismo indoor con intervalos de resistencia.")
    disc5 = Disciplina(nombre_disc="Zumba", descripcion="Baile aeróbico con ritmos latinos e internacionales.")
    disc6 = Disciplina(nombre_disc="Boxeo", descripcion="Técnicas de combate, cardio y agilidad en saco.")
    disc7 = Disciplina(nombre_disc="TRX", descripcion="Entrenamiento en suspensión usando el peso corporal.")
    disc8 = Disciplina(nombre_disc="HIIT", descripcion="Intervalos de alta intensidad para máxima quema de grasa.")
    disc9 = Disciplina(nombre_disc="Body Pump", descripcion="Entrenamiento de fuerza coreografiado con pesas ligeras.")
    disc10 = Disciplina(nombre_disc="Body Combat", descripcion="Cardio intenso con movimientos de artes marciales.")
    disc11 = Disciplina(nombre_disc="Calistenia", descripcion="Dominio del propio peso en barras y anillas.")
    disc12 = Disciplina(nombre_disc="Halterofilia", descripcion="Técnicas de levantamiento olímpico.")
    disc13 = Disciplina(nombre_disc="Stretching", descripcion="Estiramientos profundos guiados para evitar lesiones.")
    disc14 = Disciplina(nombre_disc="Step", descripcion="Coreografías aeróbicas utilizando la plataforma step.")
    disc15 = Disciplina(nombre_disc="Fitball", descripcion="Ejercicios de equilibrio y fuerza con balón suizo.")

    db.add_all([
        disc1, disc2, disc3, disc4, disc5, disc6, disc7, disc8, 
        disc9, disc10, disc11, disc12, disc13, disc14, disc15
    ])
    db.commit()