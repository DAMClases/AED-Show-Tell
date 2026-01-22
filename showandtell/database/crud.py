##########################################################
#                   CRUD OPERATIONS                      #
##########################################################

from xmlrpc import client
from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"
 
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
    '''Función que busca un usuario en la colección "alumnos" por su email.
    Function that searches for a user in the "alumnos" collection by their email.'''
    
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
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
    
    CONNECTION_STRING = "mongodb://localhost:27017/"
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
    
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    cursos = []
    for curso in db.cursos.find():
        cursos.append(curso)
    
    return cursos

def actualizar_estado_curso(alumno_id, curso_id, nuevo_estado):
    CONNECTION_STRING = "mongodb://localhost:27017/"
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
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        
        # 3. Seleccionar la base de datos
    db = client['academia']
    curso = db.cursos.find_one({"_id": curso_id})
    return curso


def obtener_informacion_perfil_usuario_alumno(mail:str):
    '''Encuentra la información asociada al usuario alumno para utilizar en el menú "Perfil de usuario"'''
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.alumnos.find_one({"email": mail})
    print(usuario)

def obtener_informacion_perfil_usuario_docente(mail:str):
    '''Encuentra la información asociada al usuario docente para utilizar en el menú "Perfil de usuario"'''
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.admin.find_one({"email": mail})
    print(usuario)

def obtener_informacion_perfil_usuario_admin(mail:str):
    '''Encuentra la información asociada al usuario admin para utilizar en el menú "Perfil de usuario"'''
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    db = client['academia']
    usuario = db.docentes.find_one({"email": mail})
    print(usuario)


obtener_informacion_perfil_usuario_alumno(mail="masangialumno005@shndtel.com")
obtener_informacion_perfil_usuario_docente(mail="jujimgardocente001@shndtel.com")
obtener_informacion_perfil_usuario_admin(mail="cristophermc@gmail.com")
