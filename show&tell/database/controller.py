#################################################################################
#                                                                               #
#                              DATABASE CONTROLLER                              #
#                                                                               #
#################################################################################

# - importations and libraries used on development

import pymongo

# - Main functionalities below

def connect_to_database()->object:
    '''
    Función que establece una conexión local al servidor local de MongoDB.
    - Devuelve un objeto base_de_datos con toda la información de los esquemas y documentos almacenados de la base de datos.
    - Más información: Esta función también crea una llamada lógica de la base de datos si no está actualmente creada. 
    La primera vez que la base de datos procese un documento, se convertirá en una entidad física.

    Function that stablishes a local connection to MongoDB's localhost Server.
    - Returns a database_object with all the information about the schemes/documents of our database.
    - More info: This function also creates a logical call of the database if it is not already created.
    The first time the database processes a document it will set off as a physical entity.'''
    
    connection_addr = pymongo.MongoClient("mongodb://localhost:27017")
    try:
        if connection_addr.admin.command('ping'):
            database_object = connection_addr['academia']
            return database_object
    except Exception as e:
        print(f"Error: {e}")

def set_up_collections(database_object)->tuple:
    '''
    Prepara y almacena todas las colecciones en una tupla. Devuelve todos los objetos para separarlos después.

    Prepares and stores all collections into a tuple. It returns all the items in order to separate them afterwards.'''

    collections_names = ('alumnos', 'cursos', 'docentes', 'matriculas', 'usuarios')
    collections = []
    for collection in collections_names:
        collections.append(database_object[collection])
    return (tuple(collection))

database_object = connect_to_database()
collections = set_up_collections(database_object)

def check_login_successfull(collections, username, passwd)->None:
    '''Comprueba desde el front de la aplicación (Menú de login) si el usuario y contraseña se encuentra
    en la colección de usuarios de la base de datos. Si los datos son encontrados, se devuelven a la capa de front
    y se procesa un cambio de ventana.
    
    Checks from the frontend layer (Login menu) if the username and password are located 
    in the users collection of the database. If data are found, they are sent back to the
    frontend layer and a new window is managed.'''
    for user in collections[4].find():
        for username, password in user:
            if username == username and passwd == passwd:
                return user
        pass