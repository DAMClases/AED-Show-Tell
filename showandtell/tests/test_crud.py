import pytest
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

# ---------------- PERFILES DE USUARIO ----------------

def test_obtener_perfil_alumno(db, datos_base):
    perfil = crud.obtener_informacion_perfil_usuario_alumno("alumno@test.com")
    assert perfil is not None
    assert perfil["nombre"] == "Pepe"

def test_obtener_perfil_docente(db, datos_base):
    perfil = crud.obtener_informacion_perfil_usuario_docente("docente@test.com")
    assert perfil is not None
    assert perfil["nombre"] == "Juan"

def test_obtener_perfil_admin(db, datos_base):
    perfil = crud.obtener_informacion_perfil_usuario_admin("admin@test.com")
    assert perfil is not None
    assert perfil["nombre"] == "Admin"

def test_obtener_perfil_inexistente(db, datos_base):
    perfil = crud.obtener_informacion_perfil_usuario_alumno("fantasma@test.com")
    assert perfil is None

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
    assert db.alumnos.find_one({"_id": "alumno_001"})["cursos"] == []

# ---------------- UTILIDADES DE CURSOS ----------------

def test_obtener_datos_cursos_concretos(db, datos_base):
    # Pasamos una lista de IDs y esperamos los objetos completos
    lista_ids = ["curso_001", "curso_002"]
    resultado = crud.obtener_datos_cursos_concretos(lista_ids)
    
    assert len(resultado) == 2
    assert resultado[0]["titulo"] == "Curso 1"
    assert resultado[1]["titulo"] == "Curso 2"

def test_actualizar_estado_curso(db, datos_base):
    crud.actualizar_estado_curso("alumno_001", "curso_001", "aprobado")
    
    alumno = db.alumnos.find_one({"_id": "alumno_001"})
    curso_alumno = next(c for c in alumno["cursos"] if c["curso"] == "curso_001")
    
    assert curso_alumno["estado"] == "aprobado"

def test_obtener_alumnos_de_un_curso(db, datos_base):
    lista_cursos = ["curso_001"]
    alumnos = crud.obtener_alumnos_de_un_curso(lista_cursos)
    
    assert len(alumnos) > 0
    assert alumnos[0]["email"] == "alumno@test.com"
    assert alumnos[0]["curso_filtrado"] == "curso_001"

def test_obtener_titulos_cursos(db, datos_base):
    lista_cursos_alumno = [{"curso": "curso_001"}, {"curso": "curso_002"}]
    titulos = crud.obtener_titulos_cursos(lista_cursos_alumno)
    
    assert "Curso 1" in titulos
    assert "Curso 2" in titulos

def test_obtener_informacion_curso_proyeccion(db, datos_base):
    info = crud.obtener_informacion_curso(["curso_001"])
    assert len(info) == 1
    assert "precio" in info[0]
    assert "titulo" not in info[0]

def test_modificar_curso_vista_docente(db, datos_base):
    datos_nuevos = ["Curso Modificado", "Desc Mod", 100, 99, "curso_001"]
    
    resultado = crud.modificar_curso_vista_docente(datos_nuevos)
    
    assert resultado is True
    curso = db.cursos.find_one({"_id": "curso_001"})
    assert curso["titulo"] == "Curso Modificado"
    assert curso["precio"] == 99
    
    docente = db.docentes.find_one({"_id": "docente_001"})
    curso_en_docente = next(c for c in docente["cursos"] if c["curso_id"] == "curso_001")
    assert curso_en_docente["titulo"] == "Curso Modificado"

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

def test_registrar_nuevo_alumno(db, datos_base):
    nuevo_alumno = {
        "nombre": "Nuevo",
        "apellidos": "Alumno",
        "email": "nuevo.alumno@test.com",
        "password": "123"
    }
    exito = crud.registrar_nuevo_alumno(nuevo_alumno)
    
    assert exito is True
    assert db.alumnos.find_one({"email": "nuevo.alumno@test.com"})

def test_obtener_recuento_alumnos_por_curso(db, datos_base):
    recuento = crud.obtener_todos_los_cursos_asociados_alumno(["curso_001", "curso_002"])
    
    assert recuento == [1, 0]

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
    assert db.cursos.find_one({"instructor.docente_id": "docente_001"}) is None
    alumno = db.alumnos.find_one({"_id": "alumno_001"})
    assert alumno["cursos"] == []

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

def test_obtener_informacion_docente_curso(db, datos_base):
    nombre_profe = crud.obtener_informacion_docente_curso("Curso 1")
    assert nombre_profe == "Juan Perez"

def test_obtener_mail_docente_nombre(db, datos_base):
    email = crud.obtener_mail_docente_nombre("Juan Perez")
    assert email == "docente@test.com"
# ---------------- UTILS ----------------

def test_get_titulo(db, datos_base):

    titulo = crud.obtener_titulo_curso("curso_001")

    assert titulo == "Curso 1"

def test_cursos_disponibles(db, datos_base):

    alumno = db.alumnos.find_one({"_id": "alumno_001"})
    cursos = crud.obtener_cursos_de_alumno(alumno['email'])
    disponibles = crud.obtener_cursos_disponibles_plataforma(cursos)

    assert len(disponibles) == 1


# ---------------- ERRORES Y REFERENCIAS INEXISTENTES ----------------

def test_crear_matricula_curso_inexistente(db, datos_base):
    with pytest.raises(ValueError) as excinfo:
        crud.crear_matricula("alumno_001", "curso_FALSO", "activo")
    
    assert "Curso no existe" in str(excinfo.value)

def test_crear_matricula_alumno_inexistente(db, datos_base):
    with pytest.raises(ValueError) as excinfo:
        crud.crear_matricula("alumno_FALSO", "curso_001", "activo")
    
    assert "Alumno no existe" in str(excinfo.value)

def test_obtener_curso_id_inexistente(db, datos_base):
    curso = crud.obtener_curso_por_id("id_falso")
    assert curso is None

def test_editar_curso_inexistente(db, datos_base):
    
    with pytest.raises(ValueError) as excinfo:
        crud.editar_curso("id_falso", "T", "D", 10, 10, "d1", "n1")

    assert "Curso no encontrado" in str(excinfo.value)

def test_eliminar_entidad_inexistente(db, datos_base):
    # MongoDB no lanza error si borras algo que no existe, simplemente retorna count 0.
    # Verificamos que no rompa la ejecución.
    try:
        crud.eliminar_curso("curso_falso_123")
        crud.eliminar_alumno("alumno_falso_123")
        crud.eliminar_docente("docente_falso_123")
    except Exception as e:
        pytest.fail(f"La eliminación de inexistentes lanzó error: {e}")

def test_actualizar_estado_curso_inexistente(db, datos_base):
    # Intentar actualizar un curso que el alumno no tiene
    crud.actualizar_estado_curso("alumno_001", "curso_002", "aprobado")
    # No debería haber cambios, verificamos que sigue igual
    alumno = db.alumnos.find_one({"_id": "alumno_001"})
    # El alumno solo tiene curso_001, curso_002 no debería haberse añadido mágicamente
    assert len(alumno["cursos"]) == 1