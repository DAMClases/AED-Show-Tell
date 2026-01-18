import pymongo
import json
from pymongo.errors import CollectionInvalid

colecciones = ('alumnos', 'matriculas', 'docentes', 'cursos', 'usuarios')
datos = {
        "_id": "alumno_011",
        "nombre": "Miguel Andrés",
        "apellidos": "López Chamarro",
        "telefono": "698755632",
        "telefono_fijo": "912456789",
        "email": "miganloalumno011@shndtel.com",
        "direccion": "Av. del Sol 45, Valencia",
        "estado": "alta",
        "fecha_alta": "2025-09-01"
        }
datos_cuentas = [
    {
    "_id": "passwd003",
    "nombre_de_usuario": "marlopsan",
    "contrasenia": "misupercontraseniasegura",
    "rol": "docente",
    "id_asociado": "docente_002",
    "email_recuperacion": "malopsadocente002@shndtel.com"
    },
    {
    "_id": "passwd004",
    "nombre_de_usuario": "carruiper",
    "contrasenia": "estoescontraseniasegura",
    "rol": "docente",
    "id_asociado": "alumno_002",
    "email_recuperacion": "caruipalumno002@shndtel.com"  
    }
]
def establecer_conexion_bd()->object:
    '''Se establece la conexión a la BBDD
    y si no hay base de datos de nombre academia
    se crea la referencia hasta que se proceda a la 
    primera creación, momento en que deja de ser una 
    referencia lógica a ser una entidad física.'''
    
    conexion = pymongo.MongoClient("mongodb://localhost:27017")
    try:
        if conexion.admin.command('ping'):
            base_de_datos = conexion['academia']
            return base_de_datos
    except Exception as e:
        print(f"Error: {e}")

def crear_colecciones(base_de_datos:object)->None:
    '''Crea las colecciones de la base de datos de manera automática.'''
    try:
        for coleccion in colecciones:
            base_de_datos.create_collection(coleccion)
    except CollectionInvalid:
        print("La colección ya existe.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
    return
#################################### CRUD (Create) #####################################
def insertar_datos_en_colecciones(base_de_datos:object)->None:
    '''Inserción automatizada y masiva de datos de prueba cargados en ficheros.'''
    try:
        for coleccion in colecciones:
            col = base_de_datos[coleccion] #transcripción del objeto
            with open(f'./data/datos_{coleccion}.json', 'r', encoding='UTF-8') as f:
                datos = json.load(f)
            if isinstance(datos, list):
                col.insert_many(datos)
            elif isinstance(datos, dict):
                col.insert_one(datos)
            else:
                print(f"Formato de datos no válido en datos_{coleccion}.json")
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
        return
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        return

def insertar_dato(base_de_datos:object, datos:dict)->None:
    '''Inserción de un solo dato concreto'''
    
    coleccion_alumnos = base_de_datos['alumnos']
    try:
        resultado = coleccion_alumnos.insert_one(datos)
    except Exception as e:
        print(f"Error > {e}")
    else:
        if resultado.inserted_id:
            print(f"Se ha insertado un dato: {resultado.inserted_id}")
            return

def insercion_varios_datos(base_de_datos:object, datos:list[dict])->None:
    coleccion_cuentas = base_de_datos['usuarios']
    try:
        resultado = coleccion_cuentas.insert_many(datos)
    except Exception as e:
        print(f"Error > {e}")
    else:
        if resultado.inserted_ids:
            print(f"Se ha insertado varios datos: {resultado.inserted_ids}")
            return
#################################### CRUD (Read) #####################################

def buscar_un_documento(base_de_datos:object)->None:
    '''Se busca un alumno cuyo teléfono tenga ese dato asociado'''
    alumnos = base_de_datos['alumnos']
    alumno = alumnos.find_one({"telefono": "687654321"})
    print(alumno)

def buscar_varios_documentos(base_de_datos:object)->None:
    '''Se busca un alumno cuyo teléfono tenga ese dato asociado'''
    alumnos = base_de_datos['alumnos']
    for alumno in alumnos.find():
        print(alumno)

def buscar_uno_varios_documentos_filtros(base_de_datos:object)->None:
    '''Se busca uno o varios cursos cuya duración en horas sea inferior a 30.
    - Los filtros aplicables son:
      - gt (mayor que)
      - eq (igual a)
      - gte (mayor o igual que)
      - lt (menor que)
      - lte (menor o igual que)'''
    cursos = base_de_datos['cursos']
    for curso in cursos.find({"duracion_horas": {"$lt": 30}}):
        print(curso)
def consulta_anidada(base_de_datos:object)->None:
    '''Usa notación de punto para recorrer una estructura anidada'''
    cursos = base_de_datos['cursos']
    for curso in cursos.find({"instructor.nombre":"Juan Jiménez García"}):
        print(curso)
def proyeccion_de_inclusion(base_de_datos:object)->None:
    '''Las proyecciones son consultas a las cuales podemos quitar alguno de los campos que no nos interesen o añadir algunos de interés
    - 1 para incluir
    - 0 para excluir de la búsqueda (_id se suele imprimir siempre)'''
    alumnos = base_de_datos[{"alumnos.alumno_id":""}]

    for alumno in alumnos.find({}, {"_id": 0, "nombre":1, "email":1}):
        print(alumno)

def proyeccion_de_exclusion(base_de_datos:object)->None:
    '''A diferencia de la otra, vamos a proyectar todos los campos menos uno.'''
    alumnos = base_de_datos['alumnos']

    for alumno in alumnos.find({}, {"_id": 0}):
        print(alumno)

def contar_todos_los_documentos(bases_de_datos:object)->None:
    '''Contamos todos los cursos que hay con un número de horas de duración mayor a 30'''

    cursos = base_de_datos['cursos']
    #TODOS LOS DOCUMENTOS
    # cursos_pedidos = cursos.count_documents({})
    # print(cursos_pedidos)
    cursos_pedidos = cursos.count_documents({"duracion_horas":{"$gt":30}})
    print(cursos_pedidos)
    
#################################### CRUD (Update) #####################################

def actualizar_un_documento(base_de_datos:object)->None:
    '''Actualizamos o buscamos actualizar un documento de una colección en específico.'''
    cursos = base_de_datos['cursos']
    resultado = cursos.update_one({"titulo":"Introducción a Java"}, {"$set": {"duracion_horas":25, "descripcion":"Curso básico para aprender Java y su IDE integrado."}})
    print(f"Documentos encontrados: {resultado.matched_count}")
    print(f"Documentos modificados: {resultado.modified_count}")

def actualizar_varios_documentos(base_de_datos:object)->None:
    '''Actualizamos o buscamos actualizar varios documentos con un filtro.'''
    cursos = base_de_datos['cursos']
    resultado = cursos.update_one({"duracion_horas":40}, {"$set": {"duracion_horas":25}})
    print(f"Documentos encontrados: {resultado.matched_count}")
    print(f"Documentos modificados: {resultado.modified_count}")

def reemplazar_documento_completo(base_de_datos:object)->None:
    '''Si tenemos una nueva pila de datos, podemos rápidamente reemplazar una antigua coincidencia de 
    datos con esta otra'''
    nuevos_datos = {
    "_id": "alumno_005",
    "nombre": "Antonia",
    "apellidos": "Santos Gil",
    "telefono": "654321098",
    "telefono_fijo": "919876543",
    "email": "masangialumno005@shndtel.com",
    "direccion": "Av. Andalucía 77, Córdoba",
    "estado": "baja",
    "fecha_alta": "2025-09-15"
    }

    alumnos = base_de_datos['alumnos']

    resultado = alumnos.replace_one({"nombre":"Marta"}, nuevos_datos)
    print(f"Documentos reemplazados: {resultado.modified_count}")

#################################### Más opciones ####################################

#Operadores de Actualización Comunes

# $set: Establecer valor
# $inc: Incrementar valor numérico
# $unset: Eliminar campo
# $push: Añadir elemento a array
# $pull: Eliminar elemento de array
# $addToSet: Añadir a array si no existe
# $rename: Renombrar campo


# EN EL DOCUMENTO DEJO MÁS OPERADORES INCLUSO. HAY QUE MIRAR BIEN.
#################################### CRUD (Delete) #####################################

def borra_un_documento(base_de_datos:object)->None:
    alumnos = base_de_datos['alumnos']
    resultado = alumnos.delete_one({"nombre": "Marta"})
    print(f"Documentos eliminados > {resultado.deleted_count}")

def borrar_muchos_documentos(base_de_datos:object)->None:
    '''Borra todos los documentos (se le pueden agregar filtros)'''
    alumnos = base_de_datos['alumnos']
    resultado = alumnos.delete_many({})
    print(f"Documentos eliminados > {resultado.deleted_count}")


    
if __name__== '__main__':
    base_de_datos = establecer_conexion_bd()
    # crear_colecciones(base_de_datos)
    # insertar_datos_en_colecciones(base_de_datos)
    # insertar_dato(base_de_datos, datos)
    # insercion_varios_datos(base_de_datos, datos_cuentas)
    # buscar_un_documento(base_de_datos)
    # buscar_varios_documentos(base_de_datos)
    # buscar_uno_varios_documentos_filtros(base_de_datos)
    # consulta_anidada(base_de_datos)
    # proyeccion_de_inclusion(base_de_datos)
    # proyeccion_de_exclusion(base_de_datos)
    # contar_todos_los_documentos(base_de_datos)
    # actualizar_un_documento(base_de_datos)
    # actualizar_varios_documentos(base_de_datos)
    # reemplazar_documento_completo(base_de_datos)
    # borrar_muchos_documentos(base_de_datos)

