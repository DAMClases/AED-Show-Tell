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