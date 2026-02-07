
from database import crud



# ---------------- AUTH ----------------

def test_login_admin(db, datos_base):

    resultado, rol = crud.buscar_usuario_por_email(
        "admin@test.com",
        "1234"
    )

    assert resultado
    assert rol == "admin"

def test_login_docente(db, datos_base):

    resultado, rol = crud.buscar_usuario_por_email(
        "docente@test.com",
        "abcd"
    )

    assert resultado
    assert rol == "docente"

def test_login_alumno(db, datos_base):

    resultado, rol = crud.buscar_usuario_por_email(
        "alumno@test.com",
        "pass"
    )

    assert resultado
    assert rol == "usuario"

def test_login_incorrecto(db):

    resultado, rol = crud.buscar_usuario_por_email(
        "no@test.com",
        "123"
    )

    assert not resultado
    assert rol == ""

# ---------------- CURSOS ----------------

def test_obtener_datos_cursos(db, datos_base):

    cursos = crud.obtener_datos_cursos()

    assert len(cursos) == 2

def test_obtener_curso_por_id(db, datos_base):

    curso = crud.obtener_curso_por_id("curso_001")

    assert curso["titulo"] == "Curso 1"
    assert curso["descripcion"] == "Basico"
    assert curso["duracion_horas"] == 40
    assert curso["precio"] == 50
    assert curso["instructor"]["docente_id"] == "docente_001"
    assert curso["instructor"]["nombre"] == "Juan Perez"

def test_crear_curso(db, datos_base):

    crud.crear_curso(
        "curso_003",
        "Java",
        "POO",
        60,
        80,
        "docente_001",
        "Juan Perez"
    )

    curso = db.cursos.find_one({"_id": "curso_003"})

    assert curso
    assert curso["titulo"] == "Java"
    assert curso["descripcion"] == "POO"
    assert curso["duracion_horas"] == 60
    assert curso["precio"] == 80
    assert curso["instructor"]["docente_id"] == "docente_001"
    assert curso["instructor"]["nombre"] == "Juan Perez"

def test_editar_curso(db, datos_base):

    crud.editar_curso(
        "curso_001",
        "Python Pro",
        "Avanzado",
        50,
        70,
        "docente_001",
        "Juan Perez"
    )

    curso = db.cursos.find_one({"_id": "curso_001"})

    assert curso["precio"] == 70
    assert curso["duracion_horas"] == 50
    assert curso["instructor"]["nombre"] == "Juan Perez"
    assert curso["titulo"] == "Python Pro"
    assert curso["descripcion"] == "Avanzado"

def test_eliminar_curso(db, datos_base):

    crud.eliminar_curso("curso_001")

    assert db.cursos.find_one({"_id": "curso_001"}) is None

# ---------------- ALUMNOS ----------------

def test_obtener_todos_los_alumnos(db, datos_base):

    alumnos = crud.obtener_todos_los_alumnos()

    assert len(alumnos) == 1

def test_eliminar_alumno(db, datos_base):

    crud.eliminar_alumno("alumno_001")

    assert db.alumnos.find_one({"_id": "alumno_001"}) is None

def test_actualizar_alumno(db, datos_base):

    crud.actualizar_alumno(
        "alumno_001",
        "Pepe2",
        "Lopez",
        "600",
        "nuevo@test.com",
        "Calle",
        "activo",
        "2026",
        "newpass"
    )

    alumno = db.alumnos.find_one({"_id": "alumno_001"})

    assert alumno["email"] == "nuevo@test.com"

# ---------------- MATRICULAS ----------------

def test_crear_matricula(db, datos_base):

    crud.crear_matricula(
        "alumno_001",
        "curso_001",
        "activo",
        "2026-01-01"
    )

    alumno = db.alumnos.find_one({"_id": "alumno_001"})

    assert len(alumno["cursos"]) == 2

def test_get_matriculas(db, datos_base):

    crud.crear_matricula(
        "alumno_001",
        "curso_002",
        "activo",
        "2026-01-01"
    )

    data = crud.obtener_todas_las_matriculas()

    assert len(data) == 2

# ---------------- DOCENTES ----------------
def test_obtener_todos_los_docentes(db, datos_base):

    docentes = crud.obtener_docentes()

    assert len(docentes) == 1

def test_eliminar_docente(db, datos_base):

    crud.eliminar_docente("docente_001")

    assert db.docentes.find_one({"_id": "docente_001"}) is None

def test_actualizar_docente(db, datos_base):
    datos_actualizados = {
        "nombre": "Cambiado1",
        "apellidos": "Cambiado2",
        "telefono": "951951951",
        "email": "cambiado@test.com",
        "direccion": "Cambiada",
        "estado": "cambiado",
        "fecha_alta": "2026-02-01",
        "password": "nuevopass"
    }
    crud.actualizar_docente(
        "docente_001",
        datos_actualizados
    )

    docente = db.docentes.find_one({"_id": "docente_001"})

    assert docente["nombre"] == "Cambiado1"
    assert docente["apellidos"] == "Cambiado2"
    assert docente["telefono"] == "951951951"
    assert docente["email"] == "cambiado@test.com"
    assert docente["direccion"] == "Cambiada"
    assert docente["estado"] == "cambiado"
    assert docente["fecha_alta"] == "2026-02-01"
    assert docente["password"] == "nuevopass"

def test_crear_docente(db, datos_base):
    datos_nuevo_docente = {
        "nombre": "Nuevo1",
        "apellidos": "Nuevo2",
        "telefono": "951951951",
        "email": "nuevo@test.com",
        "direccion": "Nueva",
        "estado": "Nuevo",
        "fecha_alta": "2026-02-01",
        "password": "nuevopass"
    }
    crud.crear_docente(datos_nuevo_docente)

    docente = db.docentes.find_one({"email": "nuevo@test.com"})

    assert docente["nombre"] == "Nuevo1"
    assert docente["apellidos"] == "Nuevo2"
    assert docente["telefono"] == "951951951"
    assert docente["direccion"] == "Nueva"
    assert docente["estado"] == "Nuevo"
    assert docente["fecha_alta"] == "2026-02-01"
    assert docente["password"] == "nuevopass"

def test_obtener_docente_por_id(db, datos_base):

    docente = crud.obtener_docente_por_id("docente_001")

    assert docente["nombre"] == "Juan"
    assert docente["apellidos"] == "Perez"
    assert docente["telefono"] == "987654321"
    assert docente["email"] == "docente@test.com"
    assert docente["direccion"] == "Avenida Falsa 456"
    assert docente["estado"] == "alta"
    assert docente["fecha_alta"] == "2024-01-01"
    assert docente["password"] == "abcd"
    assert len(docente["cursos"]) == 2
    assert docente["cursos"][0]["curso_id"] == "curso_001"
    assert docente["cursos"][0]["titulo"] == "Curso 1"
    assert docente["cursos"][1]["curso_id"] == "curso_002"
    assert docente["cursos"][1]["titulo"] == "Curso 2"

def test_obtener_todos_los_cursos_docente(db, datos_base):

    cursos = crud.obtener_todos_los_cursos_docente("docente@test.com")

    assert len(cursos) == 2
    assert cursos[0]["curso_id"] == "curso_001"
    assert cursos[0]["titulo"] == "Curso 1"
    assert cursos[1]["curso_id"] == "curso_002"
    assert cursos[1]["titulo"] == "Curso 2"
# ---------------- UTILS ----------------

def test_get_titulo(db, datos_base):

    titulo = crud.obtener_titulo_curso("curso_001")

    assert titulo == "Curso 1"

def test_cursos_disponibles(db, datos_base):

    alumno = db.alumnos.find_one({"_id": "alumno_001"})
    cursos = crud.obtener_cursos_de_alumno(alumno['email'])
    disponibles = crud.obtener_cursos_disponibles_plataforma(cursos)

    assert len(disponibles) == 1
