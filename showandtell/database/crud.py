##########################################################
#                   CRUD OPERATIONS                      #
##########################################################

from xmlrpc import client
from pymongo import MongoClient, errors

CONNECTION_STRING = "mongodb://localhost:27017/"

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
    
 
    try:
        # 2. Inicializar el cliente
        client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
        db = client['academia']
        
        # 4. Probar la conexión
        client.admin.command('ping')
        print("Conectado exitosamente al servidor LOCAL")

    except Exception as e:
        print(f"No se pudo conectar: {e}")

get_database()

def buscar_usuario_por_email(email, password) -> tuple[bool, str]:
    '''Función que busca un usuario en la colección "alumnos" por su email.'''

    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    admin = db.admin.find_one(
        {"email": email, "password": password},
        {"email": 1, "password": 1, "_id": 0}
    )
    if admin:
        return (True, "admin")
    docentes = db.docentes.find_one(
        {"email": email, "password": password},
        {"email": 1, "password": 1, "_id": 0}
    )
    if docentes:
        return (True, "docente")
    usuario = db.alumnos.find_one(
        {"email": email, "password": password},
        {"email": 1, "password": 1, "_id": 0}
    )
    if usuario:
        return (True, "usuario")
    
    return (False,"")

def obtener_todas_las_matriculas():
    '''Función que obtiene todas las matrículas de la colección "matriculas".
    Function that retrieves all enrollments from the "matriculas" collection.'''
    
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    alumnos = db.alumnos
    matriculas = []
    for alumno in alumnos.find():
        if 'cursos' in alumno:
            for curso in alumno['cursos']:
                curso_info = db.cursos.find_one({'_id': curso['curso']})
                matriculas.append({
                    'curso_id': curso['curso'],
                    'estudiante': alumno['nombre'],
                    'alumno_id': alumno['_id'],
                    'curso_nombre': curso_info['titulo'] if curso_info else 'Desconocido',
                    'fecha_matricula': curso['fecha_matricula'],
                    'status': curso['estado']
                })
    
    return matriculas

def obtener_datos_cursos() -> list:
    '''Función que obtiene todos los cursos de la colección "cursos".
    Function that retrieves all courses from the "cursos" collection.'''
    
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    cursos = []
    for curso in db.cursos.find():
        cursos.append(curso)
    
    return cursos
def obtener_datos_cursos_concretos(cursos:list)-> list:
    '''Función que obtiene todos los cursos de la colección "cursos".
    Function that retrieves all courses from the "cursos" collection.'''
    
    print("debug",cursos)
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    datos_cursos = []
    for curso in cursos:
        valor = db.cursos.find_one({'_id': curso}, {'_id':0})
        datos_cursos.append(valor)
    return datos_cursos

def actualizar_estado_curso(alumno_id, curso_id, nuevo_estado):
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    # Conectamos a la colección de alumnos
    # Buscamos al alumno por su _id Y que tenga ese curso en su lista
    filtro = {
        "_id": alumno_id, 
        "cursos.curso": curso_id
    }
    
    # Usamos el operador $ para actualizar solo el elemento del array que coincidió
    actualizacion = {
        "$set": { "cursos.$.estado": nuevo_estado }
    }
    
    db.alumnos.update_one(filtro, actualizacion)

def obtener_curso_por_id(curso_id) -> dict:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    curso = db.cursos.find_one({"_id": curso_id})
    return curso


def obtener_informacion_perfil_usuario_alumno(mail:str):
    '''Encuentra la información asociada al usuario alumno para utilizar en el menú "Perfil de usuario"'''
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.alumnos.find_one({"email": mail})
    return usuario

def obtener_informacion_perfil_usuario_docente(mail:str):
    '''Encuentra la información asociada al usuario docente para utilizar en el menú "Perfil de usuario"'''
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.docentes.find_one({"email": mail})
    return usuario

def obtener_informacion_perfil_usuario_admin(mail:str):
    '''Encuentra la información asociada al usuario admin para utilizar en el menú "Perfil de usuario"'''
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.admin.find_one({"email": mail})
    return usuario

def obtener_informacion_perfil_usuario_docente(mail:str):
    '''Encuentra la información asociada al usuario admin para utilizar en el menú "Perfil de usuario"'''
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.docentes.find_one({"email": mail})
    return usuario

def obtener_informacion_perfil_usuario_alumno(mail:str):
    '''Encuentra la información asociada al usuario alumno para utilizar en el menú "Perfil de usuario"'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.alumnos.find_one({"email": mail})
    return usuario

def crear_curso(id, titulo, descripcion, duracion, precio, docente_id, docente_nombre) -> str:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    nuevo_curso = {
        "_id": id,
        "titulo": titulo,
        "descripcion": descripcion,
        "duracion_horas": duracion,
        "precio": precio,
        "instructor": {"docente_id": docente_id, "nombre": docente_nombre}
    }
    resultado = db.cursos.insert_one(nuevo_curso)
    resultado_docente = db.docentes.update_one({"_id": docente_id},{"$push": {"cursos": {"curso_id": id, "titulo": titulo}}})    
    return resultado.inserted_id

def editar_curso(id, titulo, descripcion, duracion, precio, docente_id, docente_nombre) -> None:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    curso = obtener_curso_por_id(id)
    update_fields = {}
    if titulo != curso['titulo']:
        update_fields["titulo"] = titulo
    if descripcion != curso['descripcion']:
        update_fields["descripcion"] = descripcion
    if duracion != curso['duracion_horas']:
        update_fields["duracion_horas"] = duracion
    if precio != curso['precio']:
        update_fields["precio"] = precio
    if docente_id != curso['instructor']['docente_id'] and docente_nombre != curso['instructor']['nombre']:
        update_fields["instructor"] = {"docente_id": docente_id, "nombre": docente_nombre}

    db = client['academia']
    db.cursos.update_one(
        {"_id": id},
        {
            "$set": update_fields
        }
    )

def eliminar_curso(curso_id) -> None:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    db.cursos.delete_one({"_id": curso_id})

    # Además, eliminar el curso de la lista de cursos de los docentes
    db.docentes.update_many(
        {},
        {"$pull": {"cursos": {"curso_id": curso_id}}}
    )
    
    # Además, eliminar el curso de la lista de cursos de los alumnos
    db.alumnos.update_many(
        {},
        {"$pull": {"cursos": {"curso": curso_id}}}
    )

def crear_matricula(alumno_id, curso_id, status, fecha_matricula=None) -> None:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    nueva_matricula = {
        "curso": curso_id,
        "fecha_matricula": fecha_matricula,
        "estado": "en progreso"
    }
    db.alumnos.update_one(
        {"_id": alumno_id},
        {"$push": {"cursos": nueva_matricula}}
    )

def obtener_docentes() -> list:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    docentes = []
    for docente in db.docentes.find():
        docentes.append(docente)
    
    return docentes

def obtener_docente_por_id(docente_id) -> dict:
    
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    docente = db.docentes.find_one({"_id": docente_id})
    return docente

def registrar_nuevo_alumno(datos_alumno:dict)->bool:
    '''Registra un nuevo alumno desde el panel de administración.'''
    try:
        client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        db = client['academia']
        insercion = db.alumnos.insert_one(datos_alumno)
        if insercion.inserted_id:
            return True
        return False
    except errors.PyMongoError:
        return False

def obtener_todos_los_alumnos():
    '''Obtiene todos los alumnos registrados en la base de datos.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
    db = client['academia']
    alumnos = []
    for alumno in db.alumnos.find():
        alumnos.append(alumno)
    
    return alumnos

def get_course_name(course_id):
    curso = obtener_curso_por_id(course_id)
    return curso['titulo'] if curso else "Desconocido"



################################# 22 - 01 - 2026 : Por la tarde ####################################

def obtener_todos_los_cursos_docente(mail:str):
    '''Para el dashboard del docente y que haga bien el recuento.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    docente = db.docentes.find_one({"email":mail})
    print(docente)
    cursos = docente['cursos']
    print(cursos)
    return cursos

    

def obtener_todos_los_cursos_asociados_alumno(lista_ids:list[str])->int:
    '''Para el dashboard del docente y que haga bien el recuento de alumnos.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    recuento_alumnos = []
    for id_curso in lista_ids:
        alumnos = len(list(db.alumnos.find({"cursos.curso": id_curso})))
        recuento_alumnos.append(alumnos)
    return recuento_alumnos

def obtener_informacion_curso(lista_ids:list[str])->list[dict]:
    '''Obtiene la proyeccion de la informacion de los cursos que tiene un docente'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    info_completa = []
    for id_curso in lista_ids:
        info = db.cursos.find_one({"_id":id_curso}, {"_id":0, "titulo":0, "instructor":0})
        info_completa.append(info)
    return info_completa

def obtener_ultimo_id_curso():
    '''Como me he fijado, la función de agregar un curso, tal y como la planteamos, no agrega bien el ID
    de un curso porque MongoDB asigna una referencia distinta. Si usamos un pipeline podemos filtrar rápidamente
    cual fue el último ID que entró y luego le agregamos un procesamiento manual. 
    
    De esta forma, siempre sale correlativo y seriado.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    pipeline = [
        {"$match": {"_id": {"$regex": "^curso_"}}},
        {"$addFields": {
            "numero": {"$toInt": {"$substr": ["$_id", 6, -1]}}
        }},
        {"$group": {"_id": None, "max_num": {"$max": "$numero"}}}]
    
    resultado = list(db.cursos.aggregate(pipeline))
    
    if resultado:
        ultimo_num = resultado[0]["max_num"]
        siguiente_num = ultimo_num + 1
        print(siguiente_num)
    else:
        siguiente_num = 1
        print(siguiente_num)
    print(f"curso_{siguiente_num:03d}")
    return f"curso_{siguiente_num:03d}"

def obtener_alumnos_de_un_curso(lista_ids:list[str])->list[dict]:
    '''Devuelve una lista de diccionarios con los alumnos de un curso.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    info_completa = []
    for id_curso in lista_ids:
        info = list(db.alumnos.find({"cursos.curso":id_curso}))
        for alumno in info:
            alumno["curso_filtrado"] = id_curso
        info_completa.append(info)
    datos_de_regreso = []
    for paquete in info_completa:
        for diccionario in paquete:
            datos_de_regreso.append(diccionario)
    return(datos_de_regreso)

def obtener_titulo_curso(id_curso:str)->str:
    '''Obtiene el título de un curso dado el ID.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    datos_curso = db.cursos.find_one({"_id": id_curso})
    return datos_curso['titulo']
def obtener_titulos_cursos(lista_cursos:list[dict])->list[str]:
    '''Obtiene el título de varios cursos dado el ID recibiendo una lista de strings.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    titulos_cursos = []
    for curso in lista_cursos:
        print(curso)
        curso_id = curso['curso']
        titulo = db.cursos.find_one({"_id":curso_id}, {"_id":0, "titulo":1})
        titulos_cursos.append(titulo["titulo"])
    return titulos_cursos

    # datos_curso = db.cursos.find_one({"_id": id_curso})
    # return datos_curso['titulo']

def obtener_informacion_alumno(id_alumno:str)->str:
    '''Obtiene el título de un curso dado el ID.'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    datos_alumno = db.alumnos.find_one({"_id": id_alumno})
    return datos_alumno
def obtener_cursos_de_alumno(email:str)->list:
    '''Obtiene los cursos de un alumno'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000) 
    db = client['academia']
    info = db.alumnos.find_one({"email": email},{"cursos.curso": 1, "_id": 0})
    print(info)  
    return info
    
def obtener_cursos_disponibles_plataforma(lista_cursos:dict[list[dict]])->list:
    '''Devuelve el listado de cursos disponibles (TITULOS).'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    ids_cursos_alumno = [c['curso'] for c in lista_cursos.get('cursos', [])]
    cursos_disponibles = list(db.cursos.find({"_id": {"$nin": ids_cursos_alumno}},{"titulo": 1, "_id": 0}))
    listado_de_nombres_cursos_disponibles = []
    for curso_d in cursos_disponibles:
        listado_de_nombres_cursos_disponibles.append(curso_d["titulo"])
    return listado_de_nombres_cursos_disponibles

def obtener_informacion_docente_curso(titulo:str)->str:
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    docente = db.cursos.find_one({"titulo": titulo}, {'_id':0, 'instructor.nombre':1})
    return (docente['instructor']['nombre'])
    # return docente

def obtener_mail_docente_nombre(nombre:str)->str:
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    nombre = nombre.split(' ')
    mail = db.docentes.find_one({'nombre': nombre[0]}, {"_id":0, "email":1})
    return (mail['email'])
    # return mail

def modificar_curso_vista_docente(datos_nuevos:list)->bool:
    '''Obtiene los datos, los recopila'''
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    id_curso = datos_nuevos[4]
    titulo = datos_nuevos[0]
    descripcion = datos_nuevos[1]
    duracion = datos_nuevos[2]
    precio = datos_nuevos[3]

    resultado = db.cursos.update_one({"_id":id_curso}, {"$set": {"titulo": titulo, "descripcion": descripcion, "duracion_horas":duracion, "precio":precio}})

    return True
    # print(f"Documentos encontrados: {resultado.matched_count}")
    # print(f"Documentos modificados: {resultado.modified_count}")
        


# obtener_informacion_perfil_usuario_alumno(mail="masangialumno005@shndtel.com")


# obtener_informacion_perfil_usuario_admin(mail="cristophermc@gmail.com")
# obtener_todos_los_cursos_docente(mail="jujimgardocente001@shndtel.com")
# obtener_informacion_curso(["curso_001", "curso_002"])
# obtener_alumnos_de_un_curso(["curso_001", "curso_002"])
# obtener_titulo_curso("curso_001")
# obtener_cursos_de_alumno("anlopalumno001@shndtel.com")
# obtener_titulos_cursos([{'curso': 'curso_001'}, {'curso': 'curso_002'}])
# obtener_cursos_disponibles_plataforma(['curso_001', 'curso_002'])
# obtener_informacion_docente_curso("Introducción a Java")
# obtener_mail_docente_nombre("Juan Jiménez García")