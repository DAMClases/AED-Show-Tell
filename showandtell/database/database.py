#################################################################
#                QUICK DATABASE SETUP (PRODUCTION)              #
#################################################################

import pymongo
import json
import os
def create_database()->object:
    '''Crea la base de datos.
    
    Creates the database.'''
    connection_addr = pymongo.MongoClient("mongodb://localhost:27017")
    # Borramos las colecciones si ya existen para evitar conflictos
    db = connection_addr['academia']
    db.drop_collection('alumnos')
    db.drop_collection('cursos')
    db.drop_collection('docentes')
    db.drop_collection('usuarios')
    db.drop_collection('admin')

    # Borramos la base de datos si ya existe para evitar conflictos
    connection_addr.drop_database('academia')
    # Creamos la base de datos
    

    try:
        if connection_addr.admin.command('ping'):
            database_object = connection_addr['academia']
            return database_object
    except Exception as e:
        print(f"Error: {e}")

def create_collections(database_object:object)->tuple:
    '''Crea las colecciones de la base de datos para poder realizar pruebas en producción.
    
    It creates the needed collections for production's purpose.'''
    
    collections_names = ('alumnos', 'cursos', 'docentes', 'usuarios', 'admin')
    collections = []
    for collection in collections_names:
        collections.append(database_object[collection])
    return (tuple(collections))

def load_sample_data(collections:tuple[object])->None:
    '''Carga datos de ejemplo en las diferentes colecciones de la base de datos.
    Loads sample data into database's collections.'''

    collections_names = ('alumnos', 'cursos', 'docentes', 'usuarios', 'admin')
    current_index = 0
    try:
        print(os.getcwd())
        for collection in collections_names:
            col = collections[current_index]
            current_index +=1
            with open(f'../data/datos_{collection}.json', 'r', encoding='UTF-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                col.insert_many(data)
            elif isinstance(data, dict):
                col.insert_one(data)
            else:
                print(f"Formato de datos no válido en datos_{collection}.json.\nInvalid  for datos_{collection}.json")
        print("Los datos fueron cargados correctamente.\nAll data was loaded successfully.")

    except FileNotFoundError as e:
        print("No se ha encontrado el archivo de datos asociado.\nNo data file was found. ", e)
        return
    
if __name__ == '__main__':
    database_object = create_database()
    collections = create_collections(database_object)
    load_sample_data(collections)