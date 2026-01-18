# Guía Completa de PyMongo: MongoDB con Python

## Índice
1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Conexión a MongoDB](#conexión-a-mongodb)
4. [Bases de Datos y Colecciones](#bases-de-datos-y-colecciones)
5. [Operaciones CRUD](#operaciones-crud)
6. [Operadores de Consulta](#operadores-de-consulta)
7. [Índices](#índices)
8. [Agregaciones](#agregaciones)
9. [Operaciones Bulk](#operaciones-bulk)
10. [Paginación y Ordenamiento](#paginación-y-ordenamiento)
11. [Búsqueda de Texto Completo](#búsqueda-de-texto-completo)
12. [Transacciones](#transacciones)
13. [Manejo de Errores](#manejo-de-errores)
14. [Buenas Prácticas](#buenas-prácticas)

---

## Introducción

**PyMongo** es el driver oficial de MongoDB para Python. Permite a los desarrolladores conectarse, consultar e interactuar con bases de datos MongoDB desde aplicaciones Python de manera eficiente y pythonic.

### ¿Por qué usar PyMongo?

- **Driver oficial**: Mantenido por MongoDB Inc.
- **Compatible con frameworks**: Funciona perfectamente con Flask, Django y FastAPI
- **Alto rendimiento**: Incluye connection pooling automático
- **Completamente funcional**: Soporta todas las características de MongoDB

---

## Instalación y Configuración

### Instalación con pip

```bash
pip install pymongo
```

### Verificar la instalación

```python
import pymongo
print(pymongo.__version__)
```

### Requisitos

- Python 3.7 o superior
- MongoDB 3.6 o superior (local o en la nube como MongoDB Atlas)

---

## Conexión a MongoDB

### Conexión Básica (Local)

```python
from pymongo import MongoClient

# Conectar a MongoDB local
client = MongoClient('mongodb://localhost:27017/')

# Verificar la conexión
try:
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error de conexión: {e}")
```

### Conexión con URI

```python
from pymongo import MongoClient

# URI de conexión completa
uri = 'mongodb://localhost:27017/'
client = MongoClient(uri)
```

### Conexión con Autenticación

```python
from pymongo import MongoClient

# Método 1: URI con credenciales
uri = 'mongodb://usuario:contraseña@localhost:27017/mi_base_datos?authSource=admin'
client = MongoClient(uri)

# Método 2: Parámetros individuales
client = MongoClient(
    host='localhost',
    port=27017,
    username='usuario',
    password='contraseña',
    authSource='admin'
)
```

### Conexión a MongoDB Atlas (Cloud)

```python
from pymongo import MongoClient

# Conexión a MongoDB Atlas con URI
uri = "mongodb+srv://usuario:contraseña@cluster0.mongodb.net/mi_base_datos?retryWrites=true&w=majority"
client = MongoClient(uri)
```

### Configuración Avanzada de Conexión

```python
from pymongo import MongoClient

client = MongoClient(
    'mongodb://localhost:27017/',
    maxPoolSize=50,              # Máximo de conexiones en el pool
    minPoolSize=10,              # Mínimo de conexiones en el pool
    maxIdleTimeMS=10000,         # Tiempo máximo de inactividad
    serverSelectionTimeoutMS=5000,  # Timeout para selección de servidor
    connectTimeoutMS=10000,      # Timeout de conexión
    socketTimeoutMS=20000        # Timeout de socket
)
```

### Clase Helper para Conexión Reutilizable

```python
from pymongo import MongoClient
from contextlib import contextmanager
import os
from dotenv import load_dotenv

class MongoDBConnection:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = None
        self.db = None
    
    def connect(self, db_name):
        """Establece la conexión a la base de datos"""
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]
        return self.db
    
    def close(self):
        """Cierra la conexión"""
        if self.client:
            self.client.close()
    
    @contextmanager
    def get_collection(self, db_name, collection_name):
        """Context manager para operaciones con colecciones"""
        try:
            db = self.connect(db_name)
            yield db[collection_name]
        finally:
            self.close()

# Uso
mongo = MongoDBConnection()
with mongo.get_collection('mi_bd', 'usuarios') as collection:
    collection.insert_one({'nombre': 'Juan'})
```

---

## Bases de Datos y Colecciones

### Acceder a una Base de Datos

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Acceder a una base de datos
db = client['mi_base_datos']
# O también:
db = client.mi_base_datos
```

### Listar Bases de Datos

```python
# Listar todas las bases de datos
print(client.list_database_names())
```

### Acceder a una Colección

```python
# Acceder a una colección
coleccion = db['usuarios']
# O también:
coleccion = db.usuarios
```

### Crear una Colección

```python
# MongoDB crea la colección automáticamente al insertar el primer documento
# Pero puedes crearla explícitamente:
db.create_collection('productos')
```

### Listar Colecciones

```python
# Listar todas las colecciones de una base de datos
print(db.list_collection_names())
```

### Eliminar una Colección

```python
# Eliminar una colección completa
db.usuarios.drop()

# Verificar si existe antes de eliminar
if 'usuarios' in db.list_collection_names():
    db.usuarios.drop()
```

---

## Operaciones CRUD

### CREATE - Insertar Documentos

#### insert_one() - Insertar un solo documento

```python
# Insertar un documento
usuario = {
    "nombre": "Ana García",
    "edad": 28,
    "email": "ana@ejemplo.com",
    "activo": True
}

resultado = coleccion.insert_one(usuario)
print(f"ID insertado: {resultado.inserted_id}")
```

#### insert_many() - Insertar múltiples documentos

```python
# Insertar varios documentos
usuarios = [
    {"nombre": "Carlos López", "edad": 35, "ciudad": "Madrid"},
    {"nombre": "María Pérez", "edad": 42, "ciudad": "Barcelona"},
    {"nombre": "Juan Martín", "edad": 29, "ciudad": "Valencia"}
]

resultado = coleccion.insert_many(usuarios)
print(f"IDs insertados: {resultado.inserted_ids}")
```

### READ - Consultar Documentos

#### find_one() - Buscar un documento

```python
# Buscar un solo documento
usuario = coleccion.find_one({"nombre": "Ana García"})
print(usuario)

# Buscar por _id
from bson.objectid import ObjectId
usuario = coleccion.find_one({"_id": ObjectId("507f1f77bcf86cd799439011")})
```

#### find() - Buscar múltiples documentos

```python
# Buscar todos los documentos
for usuario in coleccion.find():
    print(usuario)

# Buscar con filtros
for usuario in coleccion.find({"edad": {"$gte": 30}}):
    print(usuario)

# Convertir a lista
usuarios = list(coleccion.find({"ciudad": "Madrid"}))
```

#### Proyecciones - Seleccionar campos específicos

```python
# Incluir solo ciertos campos (1 = incluir, 0 = excluir)
for usuario in coleccion.find({}, {"nombre": 1, "email": 1, "_id": 0}):
    print(usuario)

# Excluir campos específicos
for usuario in coleccion.find({}, {"edad": 0}):
    print(usuario)
```

#### count_documents() - Contar documentos

```python
# Contar todos los documentos
total = coleccion.count_documents({})
print(f"Total de usuarios: {total}")

# Contar con filtro
adultos = coleccion.count_documents({"edad": {"$gte": 18}})
print(f"Usuarios adultos: {adultos}")
```

### UPDATE - Actualizar Documentos

#### update_one() - Actualizar un documento

```python
# Actualizar un solo documento
resultado = coleccion.update_one(
    {"nombre": "Ana García"},           # Filtro
    {"$set": {"edad": 29, "ciudad": "Sevilla"}}  # Actualización
)

print(f"Documentos encontrados: {resultado.matched_count}")
print(f"Documentos modificados: {resultado.modified_count}")
```

#### update_many() - Actualizar múltiples documentos

```python
# Actualizar varios documentos
resultado = coleccion.update_many(
    {"ciudad": "Madrid"},               # Filtro
    {"$set": {"pais": "España"}}        # Actualización
)

print(f"Documentos modificados: {resultado.modified_count}")
```

#### replace_one() - Reemplazar un documento completo

```python
# Reemplazar completamente un documento
nuevo_usuario = {
    "nombre": "Ana García",
    "edad": 30,
    "email": "ana.nueva@ejemplo.com",
    "ciudad": "Granada"
}

resultado = coleccion.replace_one(
    {"nombre": "Ana García"},
    nuevo_usuario
)

print(f"Documentos reemplazados: {resultado.modified_count}")
```

#### Operadores de Actualización Comunes

```python
# $set: Establecer valor
coleccion.update_one({"nombre": "Juan"}, {"$set": {"edad": 35}})

# $inc: Incrementar valor numérico
coleccion.update_one({"nombre": "Juan"}, {"$inc": {"edad": 1}})

# $unset: Eliminar campo
coleccion.update_one({"nombre": "Juan"}, {"$unset": {"email": ""}})

# $push: Añadir elemento a array
coleccion.update_one(
    {"nombre": "Juan"},
    {"$push": {"hobbies": "programación"}}
)

# $pull: Eliminar elemento de array
coleccion.update_one(
    {"nombre": "Juan"},
    {"$pull": {"hobbies": "programación"}}
)

# $addToSet: Añadir a array si no existe
coleccion.update_one(
    {"nombre": "Juan"},
    {"$addToSet": {"tags": "python"}}
)

# $rename: Renombrar campo
coleccion.update_one(
    {"nombre": "Juan"},
    {"$rename": {"email": "correo_electronico"}}
)
```

### DELETE - Eliminar Documentos

#### delete_one() - Eliminar un documento

```python
# Eliminar un solo documento
resultado = coleccion.delete_one({"nombre": "Ana García"})
print(f"Documentos eliminados: {resultado.deleted_count}")
```

#### delete_many() - Eliminar múltiples documentos

```python
# Eliminar varios documentos
resultado = coleccion.delete_many({"edad": {"$lt": 18}})
print(f"Documentos eliminados: {resultado.deleted_count}")

# Eliminar todos los documentos
resultado = coleccion.delete_many({})
print(f"Todos los documentos eliminados: {resultado.deleted_count}")
```

---

## Operadores de Consulta

### Operadores de Comparación

```python
# $eq: Igual a
coleccion.find({"edad": {"$eq": 30}})
# O simplemente:
coleccion.find({"edad": 30})

# $ne: No igual a
coleccion.find({"edad": {"$ne": 30}})

# $gt: Mayor que
coleccion.find({"edad": {"$gt": 30}})

# $gte: Mayor o igual que
coleccion.find({"edad": {"$gte": 30}})

# $lt: Menor que
coleccion.find({"edad": {"$lt": 30}})

# $lte: Menor o igual que
coleccion.find({"edad": {"$lte": 30}})

# $in: Valor en lista
coleccion.find({"ciudad": {"$in": ["Madrid", "Barcelona", "Valencia"]}})

# $nin: Valor no en lista
coleccion.find({"ciudad": {"$nin": ["Madrid", "Barcelona"]}})
```

### Operadores Lógicos

```python
# $and: Operador AND
coleccion.find({
    "$and": [
        {"edad": {"$gte": 25}},
        {"ciudad": "Madrid"}
    ]
})

# O de forma implícita:
coleccion.find({"edad": {"$gte": 25}, "ciudad": "Madrid"})

# $or: Operador OR
coleccion.find({
    "$or": [
        {"ciudad": "Madrid"},
        {"ciudad": "Barcelona"}
    ]
})

# $nor: Operador NOR (ninguno de)
coleccion.find({
    "$nor": [
        {"edad": {"$lt": 18}},
        {"edad": {"$gt": 65}}
    ]
})

# $not: Negación
coleccion.find({"edad": {"$not": {"$gte": 18}}})
```

### Operadores de Elementos

```python
# $exists: Campo existe o no
coleccion.find({"email": {"$exists": True}})
coleccion.find({"telefono": {"$exists": False}})

# $type: Tipo de dato
coleccion.find({"edad": {"$type": "int"}})
coleccion.find({"edad": {"$type": "double"}})
```

### Operadores de Arrays

```python
# $all: Array contiene todos los elementos
coleccion.find({"tags": {"$all": ["python", "mongodb"]}})

# $elemMatch: Al menos un elemento coincide
coleccion.find({
    "scores": {"$elemMatch": {"$gte": 80, "$lt": 90}}
})

# $size: Tamaño del array
coleccion.find({"tags": {"$size": 3}})
```

### Operadores de Evaluación

```python
# $regex: Expresión regular
coleccion.find({"nombre": {"$regex": "^Ana"}})
coleccion.find({"email": {"$regex": "@gmail\.com$"}})

# $mod: Operación módulo
coleccion.find({"edad": {"$mod": [5, 0]}})  # Edad divisible por 5

# $text: Búsqueda de texto (requiere índice de texto)
coleccion.find({"$text": {"$search": "python programming"}})
```

### Consultas Anidadas

```python
# Documentos con estructura anidada
coleccion.insert_one({
    "nombre": "Juan",
    "direccion": {
        "calle": "Gran Vía",
        "ciudad": "Madrid",
        "codigo_postal": "28013"
    }
})

# Buscar en campos anidados usando notación de punto
coleccion.find({"direccion.ciudad": "Madrid"})
```

---

## Índices

Los índices mejoran significativamente el rendimiento de las consultas en MongoDB.

### Crear un Índice Simple

```python
# Crear índice ascendente (1) o descendente (-1)
coleccion.create_index([("nombre", 1)])

# Crear índice con nombre personalizado
coleccion.create_index(
    [("email", 1)],
    name="idx_email"
)
```

### Crear Índice Compuesto (Múltiples campos)

```python
# Índice en múltiples campos
coleccion.create_index([
    ("ciudad", 1),
    ("edad", -1)
])
```

### Crear Índice Único

```python
# Índice único (no permite duplicados)
coleccion.create_index(
    [("email", 1)],
    unique=True
)
```

### Crear Índice de Texto

```python
# Índice de texto para búsqueda full-text
coleccion.create_index(
    [("descripcion", "text")],
    default_language="spanish"
)

# Índice de texto en múltiples campos
coleccion.create_index([
    ("titulo", "text"),
    ("descripcion", "text")
])
```

### Listar Índices

```python
# Obtener información de todos los índices
for index in coleccion.list_indexes():
    print(index)
```

### Eliminar Índices

```python
# Eliminar un índice por nombre
coleccion.drop_index("idx_email")

# Eliminar todos los índices (excepto _id)
coleccion.drop_indexes()
```

### Verificar Uso de Índices (Explain)

```python
# Ver el plan de ejecución de una consulta
from pprint import pprint

explain_result = coleccion.find({"ciudad": "Madrid"}).explain()
pprint(explain_result)
```

---

## Agregaciones

El framework de agregación permite realizar operaciones complejas de procesamiento de datos.

### Pipeline de Agregación Básico

```python
# Estructura básica
pipeline = [
    {"$match": {...}},      # Filtrar documentos
    {"$group": {...}},      # Agrupar datos
    {"$sort": {...}},       # Ordenar resultados
    {"$project": {...}},    # Seleccionar campos
    {"$limit": 10}          # Limitar resultados
]

resultados = list(coleccion.aggregate(pipeline))
```

### $match - Filtrar Documentos

```python
# Filtrar antes de procesar
pipeline = [
    {"$match": {"edad": {"$gte": 18}}}
]

resultados = list(coleccion.aggregate(pipeline))
```

### $group - Agrupar y Agregar

```python
# Contar usuarios por ciudad
pipeline = [
    {
        "$group": {
            "_id": "$ciudad",
            "total": {"$sum": 1},
            "edad_promedio": {"$avg": "$edad"}
        }
    }
]

resultados = list(coleccion.aggregate(pipeline))
for resultado in resultados:
    print(f"Ciudad: {resultado['_id']}, Total: {resultado['total']}")
```

### $project - Transformar Documentos

```python
# Seleccionar y transformar campos
pipeline = [
    {
        "$project": {
            "_id": 0,
            "nombre": 1,
            "edad": 1,
            "es_mayor": {"$gte": ["$edad", 18]}
        }
    }
]

resultados = list(coleccion.aggregate(pipeline))
```

### $sort - Ordenar Resultados

```python
from bson.son import SON

# Ordenar por campo
pipeline = [
    {"$sort": SON([("edad", -1), ("nombre", 1)])}
]

resultados = list(coleccion.aggregate(pipeline))
```

### $limit y $skip - Paginación

```python
# Limitar y saltar resultados
pipeline = [
    {"$skip": 10},
    {"$limit": 5}
]

resultados = list(coleccion.aggregate(pipeline))
```

### $lookup - Join entre Colecciones

```python
# Join con otra colección
pipeline = [
    {
        "$lookup": {
            "from": "pedidos",              # Colección a unir
            "localField": "usuario_id",     # Campo local
            "foreignField": "usuario_id",   # Campo en la otra colección
            "as": "pedidos_usuario"         # Nombre del campo resultado
        }
    }
]

resultados = list(coleccion.aggregate(pipeline))
```

### $unwind - Descomponer Arrays

```python
# Descomponer un array en documentos individuales
pipeline = [
    {"$unwind": "$hobbies"}
]

resultados = list(coleccion.aggregate(pipeline))
```

### Ejemplo Completo de Agregación

```python
# Pipeline completo: análisis de ventas
pipeline = [
    # 1. Filtrar ventas del último año
    {
        "$match": {
            "fecha": {"$gte": "2024-01-01"}
        }
    },
    # 2. Agrupar por producto
    {
        "$group": {
            "_id": "$producto_id",
            "total_ventas": {"$sum": "$cantidad"},
            "ingresos": {"$sum": {"$multiply": ["$cantidad", "$precio"]}},
            "promedio_precio": {"$avg": "$precio"}
        }
    },
    # 3. Ordenar por ingresos
    {
        "$sort": {"ingresos": -1}
    },
    # 4. Limitar a top 10
    {
        "$limit": 10
    },
    # 5. Proyectar campos finales
    {
        "$project": {
            "producto_id": "$_id",
            "total_ventas": 1,
            "ingresos": {"$round": ["$ingresos", 2]},
            "promedio_precio": {"$round": ["$promedio_precio", 2]},
            "_id": 0
        }
    }
]

top_productos = list(db.ventas.aggregate(pipeline))
for producto in top_productos:
    print(producto)
```

---

## Operaciones Bulk

Las operaciones bulk permiten ejecutar múltiples operaciones en una sola llamada, mejorando significativamente el rendimiento.

### insert_many() - Inserción Masiva

```python
# Insertar muchos documentos
documentos = [{"i": i} for i in range(10000)]
resultado = coleccion.insert_many(documentos)

print(f"Documentos insertados: {len(resultado.inserted_ids)}")
```

### bulk_write() - Operaciones Mixtas

```python
from pymongo import InsertOne, UpdateOne, DeleteOne, ReplaceOne

# Preparar operaciones bulk
operaciones = [
    InsertOne({"nombre": "Carlos", "edad": 25}),
    InsertOne({"nombre": "Laura", "edad": 30}),
    UpdateOne(
        {"nombre": "Ana"},
        {"$set": {"edad": 31}}
    ),
    UpdateOne(
        {"ciudad": "Madrid"},
        {"$set": {"pais": "España"}},
        upsert=True
    ),
    DeleteOne({"edad": {"$lt": 18}}),
    ReplaceOne(
        {"nombre": "Pedro"},
        {"nombre": "Pedro González", "edad": 40}
    )
]

# Ejecutar operaciones
resultado = coleccion.bulk_write(operaciones)

print(f"Insertados: {resultado.inserted_count}")
print(f"Modificados: {resultado.modified_count}")
print(f"Eliminados: {resultado.deleted_count}")
print(f"Upserts: {resultado.upserted_count}")
```

### Bulk Write con Upsert

```python
from pymongo import UpdateOne

# Bulk upsert
operaciones = [
    UpdateOne(
        {"usuario_id": 1},
        {"$set": {"nombre": "Juan", "edad": 30}},
        upsert=True
    ),
    UpdateOne(
        {"usuario_id": 2},
        {"$set": {"nombre": "María", "edad": 25}},
        upsert=True
    ),
    UpdateOne(
        {"usuario_id": 3},
        {"$set": {"nombre": "Pedro", "edad": 35}},
        upsert=True
    )
]

resultado = coleccion.bulk_write(operaciones)
```

### Operaciones Ordenadas vs No Ordenadas

```python
from pymongo import InsertOne

operaciones = [
    InsertOne({"_id": 1, "dato": "A"}),
    InsertOne({"_id": 2, "dato": "B"}),
    InsertOne({"_id": 1, "dato": "C"}),  # Duplicado
    InsertOne({"_id": 3, "dato": "D"})
]

# Ordenadas (se detiene al primer error)
try:
    resultado = coleccion.bulk_write(operaciones, ordered=True)
except Exception as e:
    print(f"Error: {e}")

# No ordenadas (continúa pese a errores)
try:
    resultado = coleccion.bulk_write(operaciones, ordered=False)
except Exception as e:
    print(f"Error: {e}")
```

---

## Paginación y Ordenamiento

### Ordenamiento con sort()

```python
# Ordenar ascendente
for usuario in coleccion.find().sort("edad", 1):
    print(usuario)

# Ordenar descendente
for usuario in coleccion.find().sort("edad", -1):
    print(usuario)

# Ordenar por múltiples campos
for usuario in coleccion.find().sort([("ciudad", 1), ("edad", -1)]):
    print(usuario)
```

### Paginación con limit() y skip()

```python
# Primera página (10 elementos)
pagina_1 = list(coleccion.find().limit(10))

# Segunda página
pagina_2 = list(coleccion.find().skip(10).limit(10))

# Función de paginación reutilizable
def obtener_pagina(coleccion, numero_pagina, tamano_pagina=10):
    skip = (numero_pagina - 1) * tamano_pagina
    return list(coleccion.find().skip(skip).limit(tamano_pagina))

# Uso
pagina_3 = obtener_pagina(coleccion, 3, 20)
```

### Paginación Completa con Total de Documentos

```python
def paginar(coleccion, filtro={}, pagina=1, por_pagina=10):
    """
    Paginación completa con información de total de páginas
    """
    # Contar total de documentos
    total_documentos = coleccion.count_documents(filtro)
    total_paginas = (total_documentos + por_pagina - 1) // por_pagina
    
    # Calcular skip
    skip = (pagina - 1) * por_pagina
    
    # Obtener documentos de la página
    documentos = list(
        coleccion.find(filtro)
        .skip(skip)
        .limit(por_pagina)
    )
    
    return {
        "documentos": documentos,
        "pagina_actual": pagina,
        "por_pagina": por_pagina,
        "total_documentos": total_documentos,
        "total_paginas": total_paginas,
        "tiene_anterior": pagina > 1,
        "tiene_siguiente": pagina < total_paginas
    }

# Uso
resultado = paginar(coleccion, {"edad": {"$gte": 18}}, pagina=2, por_pagina=25)
print(f"Mostrando página {resultado['pagina_actual']} de {resultado['total_paginas']}")
for doc in resultado['documentos']:
    print(doc)
```

### Paginación Basada en Rangos (Más Eficiente)

```python
# Para datasets grandes, evitar skip() usando rangos
def paginar_por_rango(coleccion, ultimo_id=None, por_pagina=10):
    """
    Paginación eficiente basada en _id
    """
    filtro = {}
    if ultimo_id:
        filtro = {"_id": {"$gt": ultimo_id}}
    
    documentos = list(
        coleccion.find(filtro)
        .sort("_id", 1)
        .limit(por_pagina)
    )
    
    return documentos

# Primera página
pagina_1 = paginar_por_rango(coleccion)
ultimo_id = pagina_1[-1]["_id"] if pagina_1 else None

# Segunda página
pagina_2 = paginar_por_rango(coleccion, ultimo_id)
```

### Combinar Ordenamiento, Paginación y Filtros

```python
# Búsqueda con ordenamiento y paginación
def buscar_usuarios(filtro, orden_por="nombre", orden_dir=1, pagina=1, por_pagina=20):
    skip = (pagina - 1) * por_pagina
    
    usuarios = list(
        coleccion.find(filtro)
        .sort(orden_por, orden_dir)
        .skip(skip)
        .limit(por_pagina)
    )
    
    total = coleccion.count_documents(filtro)
    
    return {
        "usuarios": usuarios,
        "total": total,
        "pagina": pagina,
        "paginas_totales": (total + por_pagina - 1) // por_pagina
    }

# Uso
resultado = buscar_usuarios(
    {"ciudad": "Madrid"},
    orden_por="edad",
    orden_dir=-1,
    pagina=1,
    por_pagina=15
)
```

---

## Búsqueda de Texto Completo

MongoDB soporta búsqueda de texto completo mediante índices de texto.

### Crear Índice de Texto

```python
# Índice de texto en un campo
coleccion.create_index([("descripcion", "text")])

# Índice de texto en múltiples campos
coleccion.create_index([
    ("titulo", "text"),
    ("contenido", "text"),
    ("tags", "text")
])

# Índice de texto con idioma específico
coleccion.create_index(
    [("descripcion", "text")],
    default_language="spanish"
)
```

### Búsqueda Básica de Texto

```python
# Buscar documentos que contengan "python"
resultados = coleccion.find({"$text": {"$search": "python"}})

for doc in resultados:
    print(doc)
```

### Búsqueda de Frases Exactas

```python
# Buscar frase exacta usando comillas
resultados = coleccion.find({
    "$text": {"$search": '"machine learning"'}
})
```

### Búsqueda con Negación

```python
# Buscar "python" pero NO "django"
resultados = coleccion.find({
    "$text": {"$search": "python -django"}
})
```

### Búsqueda con Puntuación de Relevancia

```python
# Obtener resultados ordenados por relevancia
resultados = coleccion.find(
    {"$text": {"$search": "python mongodb"}},
    {"score": {"$meta": "textScore"}}
).sort([("score", {"$meta": "textScore"})])

for doc in resultados:
    print(f"Relevancia: {doc.get('score', 0):.2f} - {doc['titulo']}")
```

### Búsqueda de Texto en Agregaciones

```python
pipeline = [
    {
        "$match": {
            "$text": {"$search": "python programming"}
        }
    },
    {
        "$project": {
            "titulo": 1,
            "score": {"$meta": "textScore"}
        }
    },
    {
        "$sort": {"score": {"$meta": "textScore"}}
    },
    {
        "$limit": 10
    }
]

resultados = list(coleccion.aggregate(pipeline))
```

### Ejemplo Completo de Búsqueda

```python
# Crear colección de artículos
articulos = db.articulos

# Insertar datos de ejemplo
articulos.insert_many([
    {
        "titulo": "Introducción a Python",
        "contenido": "Python es un lenguaje de programación interpretado...",
        "tags": ["python", "programación", "tutorial"]
    },
    {
        "titulo": "MongoDB y Python",
        "contenido": "PyMongo es el driver oficial de MongoDB para Python...",
        "tags": ["python", "mongodb", "bases de datos"]
    },
    {
        "titulo": "Machine Learning con Python",
        "contenido": "Python ofrece excelentes librerías para machine learning...",
        "tags": ["python", "ml", "inteligencia artificial"]
    }
])

# Crear índice de texto
articulos.create_index([
    ("titulo", "text"),
    ("contenido", "text"),
    ("tags", "text")
])

# Buscar
resultados = articulos.find(
    {"$text": {"$search": "python mongodb"}},
    {"score": {"$meta": "textScore"}}
).sort([("score", {"$meta": "textScore"})])

print("Resultados de búsqueda:")
for articulo in resultados:
    print(f"- {articulo['titulo']} (relevancia: {articulo['score']:.2f})")
```

---

## Transacciones

Las transacciones permiten ejecutar múltiples operaciones de forma atómica (todo o nada).

**Nota**: Las transacciones requieren MongoDB 4.0+ y un replica set o cluster sharded.

### Transacción Básica

```python
# Iniciar una sesión
with client.start_session() as session:
    # Iniciar transacción
    with session.start_transaction():
        try:
            # Operaciones dentro de la transacción
            db.cuentas.update_one(
                {"usuario": "Ana"},
                {"$inc": {"saldo": -100}},
                session=session
            )
            
            db.cuentas.update_one(
                {"usuario": "Carlos"},
                {"$inc": {"saldo": 100}},
                session=session
            )
            
            # Si todo va bien, se commitea automáticamente
            print("Transacción completada")
            
        except Exception as e:
            # Si hay error, se aborta automáticamente
            print(f"Error en transacción: {e}")
            raise
```

### Transacción con Callback

```python
def transferir_dinero(session):
    """
    Función callback para ejecutar dentro de una transacción
    """
    cuentas = session.client.db.cuentas
    
    # Verificar saldo suficiente
    cuenta_origen = cuentas.find_one(
        {"usuario": "Ana"},
        session=session
    )
    
    if cuenta_origen["saldo"] < 100:
        raise ValueError("Saldo insuficiente")
    
    # Realizar transferencia
    cuentas.update_one(
        {"usuario": "Ana"},
        {"$inc": {"saldo": -100}},
        session=session
    )
    
    cuentas.update_one(
        {"usuario": "Carlos"},
        {"$inc": {"saldo": 100}},
        session=session
    )
    
    return "Transferencia exitosa"

# Ejecutar transacción con callback
with client.start_session() as session:
    resultado = session.with_transaction(transferir_dinero)
    print(resultado)
```

### Manejo de Errores en Transacciones

```python
from pymongo.errors import ConnectionFailure, OperationFailure

def ejecutar_con_retry(functor, session):
    """
    Ejecuta una transacción con reintentos automáticos
    """
    while True:
        try:
            with session.start_transaction():
                resultado = functor(session)
                # Commit con retry
                while True:
                    try:
                        session.commit_transaction()
                        break
                    except Exception as exc:
                        if exc.has_error_label("UnknownTransactionCommitResult"):
                            print("Reintentando commit...")
                            continue
                        raise
                break
        except (ConnectionFailure, OperationFailure) as exc:
            # Error transitorio, reintentar toda la transacción
            if exc.has_error_label("TransientTransactionError"):
                print("Error transitorio, reintentando transacción...")
                continue
            raise
    
    return resultado

# Uso
with client.start_session() as session:
    resultado = ejecutar_con_retry(transferir_dinero, session)
    print(resultado)
```

### Ejemplo Completo: Sistema de Reservas

```python
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.reservas_db

def reservar_asiento(usuario_id, vuelo_id, asiento_num):
    """
    Reserva un asiento de forma transaccional
    """
    with client.start_session() as session:
        def callback(session):
            # 1. Verificar disponibilidad
            asiento = db.asientos.find_one(
                {"vuelo_id": vuelo_id, "numero": asiento_num},
                session=session
            )
            
            if not asiento or asiento.get("reservado"):
                raise ValueError(f"Asiento {asiento_num} no disponible")
            
            # 2. Marcar asiento como reservado
            db.asientos.update_one(
                {"vuelo_id": vuelo_id, "numero": asiento_num},
                {"$set": {"reservado": True, "usuario_id": usuario_id}},
                session=session
            )
            
            # 3. Crear registro de pago
            db.pagos.insert_one(
                {
                    "usuario_id": usuario_id,
                    "vuelo_id": vuelo_id,
                    "asiento": asiento_num,
                    "monto": 150.00,
                    "fecha": datetime.utcnow()
                },
                session=session
            )
            
            # 4. Actualizar auditoría
            db.auditoria.insert_one(
                {
                    "accion": "reserva",
                    "usuario_id": usuario_id,
                    "vuelo_id": vuelo_id,
                    "asiento": asiento_num,
                    "timestamp": datetime.utcnow()
                },
                session=session
            )
            
            return f"Asiento {asiento_num} reservado exitosamente"
        
        # Ejecutar con reintentos automáticos
        return session.with_transaction(callback)

# Uso
try:
    resultado = reservar_asiento(
        usuario_id="user123",
        vuelo_id="EI178",
        asiento_num="12A"
    )
    print(resultado)
except Exception as e:
    print(f"Error en reserva: {e}")
```

---

## Manejo de Errores

### Excepciones Comunes

```python
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError,
    OperationFailure,
    DuplicateKeyError,
    WriteError,
    PyMongoError
)

# Capturar todas las excepciones de PyMongo
try:
    resultado = coleccion.insert_one({"email": "duplicado@test.com"})
except PyMongoError as e:
    print(f"Error de PyMongo: {e}")
```

### Manejo de Errores de Conexión

```python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    client = MongoClient(
        'mongodb://localhost:27017/',
        serverSelectionTimeoutMS=5000
    )
    # Probar conexión
    client.admin.command('ping')
    print("Conexión exitosa")
    
except ServerSelectionTimeoutError:
    print("No se pudo conectar al servidor MongoDB")
    print("Verifica que MongoDB esté ejecutándose")
    
except ConnectionFailure as e:
    print(f"Fallo de conexión: {e}")
```

### Manejo de Errores de Escritura

```python
from pymongo.errors import DuplicateKeyError, WriteError

# Error de clave duplicada
try:
    coleccion.insert_one({"_id": 1, "nombre": "Juan"})
    coleccion.insert_one({"_id": 1, "nombre": "Ana"})  # Error
except DuplicateKeyError:
    print("El documento con ese _id ya existe")

# Errores de validación
try:
    resultado = coleccion.update_one(
        {"nombre": "Juan"},
        {"$set": {"edad": "treinta"}}  # Tipo incorrecto si hay validación
    )
except WriteError as e:
    print(f"Error de escritura: {e.details}")
```

### Manejo de Errores en Operaciones Bulk

```python
from pymongo import InsertOne
from pymongo.errors import BulkWriteError

operaciones = [
    InsertOne({"_id": 1, "dato": "A"}),
    InsertOne({"_id": 2, "dato": "B"}),
    InsertOne({"_id": 1, "dato": "C"}),  # Duplicado
]

try:
    resultado = coleccion.bulk_write(operaciones, ordered=False)
    print(f"Insertados: {resultado.inserted_count}")
    
except BulkWriteError as bwe:
    print(f"Errores encontrados: {len(bwe.details['writeErrors'])}")
    print(f"Insertados exitosamente: {bwe.details['nInserted']}")
    
    # Detalles de errores
    for error in bwe.details['writeErrors']:
        print(f"Error en índice {error['index']}: {error['errmsg']}")
```

### Patrón Completo de Manejo de Errores

```python
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)

def operacion_segura(coleccion, documento):
    """
    Realiza una operación con manejo completo de errores
    """
    try:
        # Intentar insertar
        resultado = coleccion.insert_one(documento)
        return {
            "exito": True,
            "id": resultado.inserted_id,
            "mensaje": "Documento insertado correctamente"
        }
        
    except ConnectionFailure:
        return {
            "exito": False,
            "error": "connection",
            "mensaje": "No se pudo conectar a MongoDB"
        }
        
    except DuplicateKeyError as e:
        return {
            "exito": False,
            "error": "duplicate",
            "mensaje": "El documento ya existe",
            "detalles": str(e)
        }
        
    except OperationFailure as e:
        return {
            "exito": False,
            "error": "operation",
            "mensaje": f"Error en la operación: {e.details}",
            "codigo": e.code
        }
        
    except PyMongoError as e:
        return {
            "exito": False,
            "error": "pymongo",
            "mensaje": f"Error de PyMongo: {str(e)}"
        }
        
    except Exception as e:
        return {
            "exito": False,
            "error": "unknown",
            "mensaje": f"Error inesperado: {str(e)}"
        }

# Uso
resultado = operacion_segura(coleccion, {"nombre": "Test"})
if resultado["exito"]:
    print(f"✓ {resultado['mensaje']}")
else:
    print(f"✗ Error ({resultado['error']}): {resultado['mensaje']}")
```

### Reintentos Automáticos

```python
import time
from pymongo.errors import AutoReconnect

def ejecutar_con_reintentos(funcion, max_reintentos=3, delay=1):
    """
    Ejecuta una función con reintentos automáticos
    """
    for intento in range(max_reintentos):
        try:
            return funcion()
        except AutoReconnect:
            if intento < max_reintentos - 1:
                print(f"Reintento {intento + 1}/{max_reintentos}...")
                time.sleep(delay)
            else:
                raise
    
# Uso
def mi_operacion():
    return coleccion.find_one({"nombre": "Juan"})

try:
    resultado = ejecutar_con_reintentos(mi_operacion)
    print(resultado)
except AutoReconnect:
    print("No se pudo reconectar después de varios intentos")
```

---

## Buenas Prácticas

### 1. Gestión de Conexiones

```python
# ✓ BIEN: Reutilizar cliente
client = MongoClient('mongodb://localhost:27017/')
db = client.mi_base_datos

# Usar en toda la aplicación
def operacion_1():
    coleccion = db.usuarios
    # ...

def operacion_2():
    coleccion = db.pedidos
    # ...

# ✗ MAL: Crear cliente en cada función
def operacion_mal():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.mi_base_datos
    # ...
```

### 2. Usar Connection Pooling

```python
# Configurar pool de conexiones adecuadamente
client = MongoClient(
    'mongodb://localhost:27017/',
    maxPoolSize=50,      # Ajustar según carga
    minPoolSize=10,
    maxIdleTimeMS=45000
)
```

### 3. Indexar Campos de Consulta Frecuente

```python
# Crear índices para consultas comunes
coleccion.create_index([("email", 1)], unique=True)
coleccion.create_index([("fecha_creacion", -1)])
coleccion.create_index([("ciudad", 1), ("edad", 1)])

# Verificar uso de índices
explain = coleccion.find({"email": "test@test.com"}).explain()
```

### 4. Proyecciones para Optimizar

```python
# ✓ BIEN: Seleccionar solo campos necesarios
usuarios = coleccion.find(
    {"ciudad": "Madrid"},
    {"nombre": 1, "email": 1, "_id": 0}
)

# ✗ MAL: Traer todo el documento
usuarios = coleccion.find({"ciudad": "Madrid"})
```

### 5. Usar Variables de Entorno para Credenciales

```python
import os
from dotenv import load_dotenv

load_dotenv()

# ✓ BIEN: Credenciales en variables de entorno
MONGO_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGO_URI)

# ✗ MAL: Credenciales hardcodeadas
# client = MongoClient('mongodb://user:pass123@localhost:27017/')
```

### 6. Validación de Datos

```python
# Validar datos antes de insertar
def crear_usuario(datos):
    # Validación
    if not datos.get('email'):
        raise ValueError("Email es requerido")
    
    if not isinstance(datos.get('edad'), int):
        raise ValueError("Edad debe ser un número entero")
    
    # Insertar
    return coleccion.insert_one(datos)
```

### 7. Manejo Apropiado de ObjectId

```python
from bson.objectid import ObjectId

# ✓ BIEN: Convertir string a ObjectId
usuario_id = "507f1f77bcf86cd799439011"
usuario = coleccion.find_one({"_id": ObjectId(usuario_id)})

# ✗ MAL: Usar string directamente
# usuario = coleccion.find_one({"_id": usuario_id})  # No encontrará nada
```

### 8. Limitar Resultados en Queries

```python
# ✓ BIEN: Limitar resultados
usuarios = list(coleccion.find().limit(100))

# ✗ MAL: Traer todos los documentos sin límite
# usuarios = list(coleccion.find())  # Puede ser millones
```

### 9. Usar Operaciones Bulk para Múltiples Escrituras

```python
from pymongo import InsertOne

# ✓ BIEN: Bulk insert
operaciones = [InsertOne({"i": i}) for i in range(10000)]
coleccion.bulk_write(operaciones)

# ✗ MAL: Inserts individuales
# for i in range(10000):
#     coleccion.insert_one({"i": i})  # Muy lento
```

### 10. Cerrar Conexiones Correctamente

```python
# ✓ BIEN: Usar context manager o cerrar explícitamente
try:
    client = MongoClient('mongodb://localhost:27017/')
    # Operaciones...
finally:
    client.close()

# O mejor aún, context manager personalizado
from contextlib import contextmanager

@contextmanager
def mongo_connection(uri):
    client = MongoClient(uri)
    try:
        yield client
    finally:
        client.close()

# Uso
with mongo_connection('mongodb://localhost:27017/') as client:
    db = client.mi_base_datos
    # Operaciones...
```

### 11. Estructura de Proyecto Recomendada

```
proyecto/
├── config/
│   ├── __init__.py
│   └── database.py          # Configuración de conexión
├── models/
│   ├── __init__.py
│   └── usuario.py           # Modelos/schemas
├── services/
│   ├── __init__.py
│   └── usuario_service.py   # Lógica de negocio
├── utils/
│   ├── __init__.py
│   └── db_helpers.py        # Helpers de BD
├── .env                      # Variables de entorno
├── requirements.txt
└── main.py
```

**config/database.py:**
```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(
                os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'),
                maxPoolSize=50,
                minPoolSize=10
            )
            cls._instance.db = cls._instance.client[os.getenv('DB_NAME', 'mi_bd')]
        return cls._instance
    
    def get_collection(self, name):
        return self.db[name]
    
    def close(self):
        if self.client:
            self.client.close()

# Singleton
db = Database()
```

**services/usuario_service.py:**
```python
from config.database import db
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

class UsuarioService:
    def __init__(self):
        self.coleccion = db.get_collection('usuarios')
        # Crear índices
        self.coleccion.create_index([("email", 1)], unique=True)
    
    def crear_usuario(self, datos):
        try:
            resultado = self.coleccion.insert_one(datos)
            return {"exito": True, "id": str(resultado.inserted_id)}
        except DuplicateKeyError:
            return {"exito": False, "error": "Email ya existe"}
    
    def obtener_usuario(self, usuario_id):
        return self.coleccion.find_one({"_id": ObjectId(usuario_id)})
    
    def actualizar_usuario(self, usuario_id, datos):
        resultado = self.coleccion.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": datos}
        )
        return resultado.modified_count > 0
    
    def eliminar_usuario(self, usuario_id):
        resultado = self.coleccion.delete_one({"_id": ObjectId(usuario_id)})
        return resultado.deleted_count > 0
    
    def listar_usuarios(self, filtro={}, pagina=1, por_pagina=20):
        skip = (pagina - 1) * por_pagina
        usuarios = list(
            self.coleccion.find(filtro)
            .skip(skip)
            .limit(por_pagina)
        )
        total = self.coleccion.count_documents(filtro)
        
        return {
            "usuarios": usuarios,
            "total": total,
            "pagina": pagina,
            "total_paginas": (total + por_pagina - 1) // por_pagina
        }
```

---

## Recursos Adicionales

### Documentación Oficial

- **PyMongo Documentation**: https://pymongo.readthedocs.io/
- **MongoDB Manual**: https://docs.mongodb.com/manual/
- **MongoDB Python Driver**: https://docs.mongodb.com/drivers/python/

### Tutoriales y Cursos

- DataCamp: Introduction to Using MongoDB for Data Science with Python
- MongoDB University: MongoDB for Python Developers
- Real Python: Introduction to MongoDB and Python

### Herramientas Útiles

- **MongoDB Compass**: GUI oficial para MongoDB
- **Studio 3T**: IDE profesional para MongoDB
- **Robo 3T**: Cliente ligero para MongoDB

### Comunidad

- Stack Overflow: Tag `pymongo`
- MongoDB Community Forums
- GitHub: mongodb/mongo-python-driver

---

## Conclusión

Esta guía cubre los aspectos fundamentales y avanzados de PyMongo para trabajar con MongoDB en Python. Los temas principales incluyen:

- ✓ Conexión y configuración
- ✓ Operaciones CRUD completas
- ✓ Consultas y operadores avanzados
- ✓ Índices para optimización
- ✓ Agregaciones complejas
- ✓ Operaciones bulk
- ✓ Paginación eficiente
- ✓ Búsqueda de texto completo
- ✓ Transacciones ACID
- ✓ Manejo robusto de errores
- ✓ Buenas prácticas de producción

Con estos conocimientos, estás preparado para desarrollar aplicaciones robustas y escalables usando MongoDB y Python. ¡Buena suerte con tus proyectos!

---

**Versión**: 1.0  
**Última actualización**: Enero 2026  
**Autor**: Guía completa de PyMongo  
**Licencia**: Uso educativo
