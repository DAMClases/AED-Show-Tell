#################################################################
#                QUICK DATABASE SETUP (PRODUCTION)              #
#################################################################

import pymongo
import json
import os
def crear_base_de_datos()->object:
    '''Crea la base de datos.'''
    direccion_conexion_base_datos = pymongo.MongoClient("mongodb://localhost:27017")

    db = direccion_conexion_base_datos['academia']
    db.drop_collection('alumnos')
    db.drop_collection('cursos')
    db.drop_collection('docentes')
    db.drop_collection('usuarios')
    db.drop_collection('admin')

    direccion_conexion_base_datos.drop_database('academia')
    

    try:
        if direccion_conexion_base_datos.admin.command('ping'):
            objeto_conexion = direccion_conexion_base_datos['academia']
            return objeto_conexion
    except Exception as e:
        print(f"Error: {e}")

def crear_colecciones(objeto_conexion:object)->tuple:
    '''Crea las colecciones de la base de datos para poder realizar pruebas en producción.'''
    
    colecciones = ('alumnos', 'cursos', 'docentes', 'usuarios', 'admin')
    col = []
    for c in colecciones:
        col.append(objeto_conexion[c])
    return (tuple(col))

def cargar_datos(col:tuple[object])->None:
    '''Carga datos de ejemplo en las diferentes colecciones de la base de datos.'''

    colecciones = ('alumnos', 'cursos', 'docentes', 'usuarios', 'admin')
    indice = 0
    try:
        print(os.getcwd())
        for c in colecciones:
            col = col[indice]
            indice +=1
            with open(f'../data/datos_{c}.json', 'r', encoding='UTF-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                col.insert_many(data)
            elif isinstance(data, dict):
                col.insert_one(data)
            else:
                print(f"Formato de datos no válido en datos_{c}.json.\nInvalid  for datos_{c}.json")
        print("Los datos fueron cargados correctamente.\nAll data was loaded successfully.")

    except FileNotFoundError as e:
        print("No se ha encontrado el archivo de datos asociado.\nNo data file was found. ", e)
        return
    
if __name__ == '__main__':
    objeto_conexion = crear_base_de_datos()
    col = crear_colecciones(objeto_conexion)
    cargar_datos(col)