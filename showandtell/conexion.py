import pymongo
'''Los dos argumentos a continuación representan la conexión del host y 
el puerto de escucha de MongoDB'''
try:
    cliente = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
#ping de conexión
    print(cliente.admin.command("ping"))
    print("Conexion hecha.")
    print(cliente.admin.command("listDatabases"))
    base_de_datos = cliente['academia']
    base_de_datos = cliente.academia
    alumnos = base_de_datos.clientes
    print(base_de_datos)
    print(alumnos)
    print("--------------------")
    print(base_de_datos.list_collection_names()) #LISTA las colecciones de la base de datos
    print("Listado de datos de una colección: ")
    docentes = base_de_datos['docentes']
    for usuario in docentes.find():
        print(usuario)
    print("Listado por filtros (PROYECCIONES): ")
    for usuario in docentes.find({}, {"estado":"alta"}):
        print(usuario)
    #Operación de inclusión y exclusión (1 = incluir, 0 = excluir):
    for usuario in docentes.find({}, {"_id":0, "nombre":1, "apellidos":1}):
        print(usuario)
        if usuario['nombre'] == 'Juan':
            print(usuario['apellidos'])











            ######################################## CRUD #####################################

except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Error: {e}")

