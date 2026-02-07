import pytest
from pymongo import MongoClient
from database import crud


URI = "mongodb://localhost:27017/"
DB_NAME = "academia_test"


@pytest.fixture(scope="function")
def db():

    client = MongoClient(URI)

    client.drop_database(DB_NAME)

    database = client[DB_NAME]

    crud.init_db(database)

    yield database

    client.drop_database(DB_NAME)

    client.close()


@pytest.fixture
def datos_base(db):

    db.admin.insert_one({
        "_id": "admin_001",
        "nombre": "Admin",
        "apellidos": "Test",
        "telefono": "123456789",
        "email": "admin@test.com",
        "direccion": "Calle Falsa 123",
        "password": "1234"
    })

    db.docentes.insert_one({
        "_id": "docente_001",
        "nombre": "Juan",
        "apellidos": "Perez",
        "telefono": "987654321",
        "email": "docente@test.com",
        "direccion": "Avenida Falsa 456",
        "estado": "alta",
        "fecha_alta": "2024-01-01",
        "password": "abcd",
        "cursos": [
            { "curso_id": "curso_001", "titulo": "Curso 1" },
            { "curso_id": "curso_002", "titulo": "Curso 2" }
        ]
    })

    db.cursos.insert_many([
        {
            "_id": "curso_001",
            "titulo": "Curso 1",
            "descripcion": "Basico",
            "duracion_horas": 40,
            "precio": 50,
        "instructor": {
            "docente_id": "docente_001",
            "nombre": "Juan Perez"
        }
        },
        {
            "_id": "curso_002",
            "titulo": "Curso 2",
            "descripcion": "Intermedio",
            "duracion_horas": 60,
            "precio": 70,
        "instructor": {
            "docente_id": "docente_001",
            "nombre": "Juan Perez"
        }
    }])

    db.alumnos.insert_one({
        "_id": "alumno_001",
        "nombre": "Pepe",
        "apellidos": "Gomez",
        "telefono": "555555555",
        "email": "alumno@test.com",
        "direccion": "Calle Falsa 789",
        "estado": "alta",
        "fecha_alta": "2024-01-01",
        "password": "pass",
        "cursos": [
            { "curso": "curso_001", "fecha_matricula":"27/03/2025", "estado":"pendiente"}]
    })
