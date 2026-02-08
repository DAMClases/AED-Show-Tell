import flet as ft
from database.crud import *
from utils.elements import *
from utils.validaciones import *

contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_vista_cursos_admin():
    
    datos_cursos = obtener_datos_cursos()
    from utils.elements import tarjeta_curso
    course_cards = [tarjeta_curso(page,curso) for curso in datos_cursos]
    contenedor.content = ft.Column([
        ft.Row([
        ft.Text("Gestión de Cursos", size=30, weight="bold"),
        ft.Button("Agregar Nuevo Curso", icon=ft.Icons.ADD, on_click=lambda e: mostrar_añadir_curso_dialog())
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Row(course_cards, wrap=True, spacing=20, run_spacing=20)
    ], scroll="auto")
    contenedor.update()

def mostrar_añadir_curso_dialog():
    from utils.elements import autocompletar_campo
    titulo = ft.TextField(label="Título del curso")
    descripcion = ft.TextField(label="Descripción", multiline=True)
    precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
    duracion = ft.TextField(label="Duración (horas)", keyboard_type=ft.KeyboardType.NUMBER)
    
    docente_id_seleccionado = None

    def set_docente(docente_id):
        nonlocal docente_id_seleccionado
        docente_id_seleccionado = docente_id
    
    docente_id = autocompletar_campo(set_docente, "Docente")

    def guardar_curso(e):

        if not titulo.value or not descripcion.value or not precio.value or not duracion.value:
            mostrar_mensaje(page, "Alguno de los campos se encuentran vacíos. Por favor, rellénelos previamente antes de continuar.", "advertencia")
            return
        if not validar_entrada_precio(precio.value):
            mostrar_mensaje(page, "El precio de un curso debe ser mayor que 0.", "advertencia")
            return
        if not validar_entrada_duracion(duracion.value):
            mostrar_mensaje(page, "La duración de un curso debe ser mayor que 0.", "advertencia")
            return
        if obtener_docente_por_id(docente_id_seleccionado) is None:
            mostrar_mensaje(page, "El docente seleccionado no existe. Por favor, seleccione un docente válido.", "advertencia")
            return
            
        precio_str = precio.value.replace(',', '.')
        precio_valor = float(precio_str)
        id_curso_correlativo = obtener_ultimo_id_curso()
        crear_curso(
            id = id_curso_correlativo,
            titulo=titulo.value,
            descripcion=descripcion.value,
            precio=precio_valor,
            duracion=int(duracion.value),
            docente_id=docente_id_seleccionado,
            docente_nombre=obtener_docente_por_id(docente_id_seleccionado)['nombre'] + " " + obtener_docente_por_id(docente_id_seleccionado)['apellidos']
        )
        mostrar_mensaje(page, "Nuevo curso implementado correctamente en el sistema.", "info")
        dlg.open = False
        cargar_vista_cursos_admin()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Agregar Nuevo Curso"),
        content=ft.Column([
            titulo,
            descripcion,
            precio,
            duracion,
            docente_id
        ], tight=True),
        actions=[
            ft.Button("Guardar", on_click=guardar_curso),
            ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
        ]
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def mostrar_editar_curso_dialog(curso_id, dlg_detalles_curso):
    curso = obtener_curso_por_id(curso_id)
    from utils.elements import autocompletar_campo
    titulo = ft.TextField(label="Título del curso")
    descripcion = ft.TextField(label="Descripción", multiline=True)
    precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
    duracion = ft.TextField(label="Duración (horas)", keyboard_type=ft.KeyboardType.NUMBER)

    titulo.value = curso['titulo']
    descripcion.value = curso['descripcion']
    precio.value = str(curso['precio'])
    duracion.value = str(curso['duracion_horas'])

    def set_docente(docente_id):
        nonlocal docente_id_seleccionado
        docente_id_seleccionado = docente_id

    docente_id = autocompletar_campo(set_docente, "Docente", curso['instructor']['nombre'])

    docente_id_seleccionado = curso['instructor']['docente_id']

    def editar_curso_info(e, dlg_detalles_curso):

        if not titulo.value or not descripcion.value or not precio.value or not duracion.value:
            mostrar_mensaje(page, "Alguno de los campos se encuentran vacíos. Por favor, rellénelos previamente antes de continuar.", "advertencia")
            return
        if not validar_entrada_precio(precio.value):
            mostrar_mensaje(page, "El precio de un curso debe ser mayor que 0.", "advertencia")
            return
        if not validar_entrada_duracion(duracion.value):
            mostrar_mensaje(page, "La duración de un curso debe ser mayor que 0.", "advertencia")
            return
        precio_str = precio.value.replace(',', '.')
        precio_valor = float(precio_str)
        id_curso_correlativo = curso['_id']
        editar_curso(
            id = id_curso_correlativo,
            titulo=titulo.value,
            descripcion=descripcion.value,
            precio=precio_valor,
            duracion=int(duracion.value),
            docente_id=docente_id_seleccionado,
            docente_nombre=obtener_docente_por_id(docente_id_seleccionado)['nombre'] + " " + obtener_docente_por_id(docente_id_seleccionado)['apellidos']
        )
        mostrar_mensaje(page, "Nuevo curso implementado correctamente en el sistema.", "info")
        dlg.open = False
        detalles_col = dlg_detalles_curso.content
        dlg_detalles_curso.content.controls = [
            ft.Text(f"ID: {id_curso_correlativo}"),
            ft.Text(f"Descripción: {descripcion.value}"),
            ft.Text(f"Precio: ${precio_valor:.2f}"),
            ft.Text(f"Duración: {duracion.value} horas"),
            ft.Text(f"Instructor: {obtener_docente_por_id(docente_id_seleccionado)['nombre'] + ' ' + obtener_docente_por_id(docente_id_seleccionado)['apellidos']}"
            ),
        ]
        dlg_detalles_curso.title = ft.Text(f"Detalles del Curso: {titulo.value}")
        cargar_vista_cursos_admin()
        dlg_detalles_curso.update()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Editar Curso"),
        content=ft.Column([
            titulo,
            descripcion,
            precio,
            duracion,
            docente_id
        ], tight=True),
        actions=[
            ft.Button("Actualizar", on_click=lambda e: editar_curso_info(e, dlg_detalles_curso)),
            ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
        ]
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def mostrar_detalles_curso(curso_id):
    curso = obtener_curso_por_id(curso_id)
    if not curso:
        print(f"Curso con ID {curso_id} no encontrado.")
        return

    dlg = ft.AlertDialog(
        title=ft.Text(f"Detalles del Curso: {curso['titulo']}"),
        content=ft.Column([
            ft.Text(f"ID: {curso['_id']}"),
            ft.Text(f"Descripción: {curso['descripcion']}"),
            ft.Text(f"Precio: ${curso['precio']:.2f}"),
            ft.Text(f"Duración: {curso['duracion_horas']} horas"),
            ft.Text(f"Instructor: {curso['instructor']['nombre']}"),
        ], spacing=10),
        actions=[
            ft.Button("Editar", icon=ft.Icons.EDIT, on_click=lambda e: mostrar_editar_curso_dialog(curso_id,dlg)),
            ft.Button("Borrar", icon=ft.Icons.DELETE, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: (mostrar_confirmacion_eliminar_curso(curso_id), setattr(dlg, "open", False), page.update())),
            ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
        ],
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def mostrar_confirmacion_eliminar_curso(curso_id):
    curso = obtener_curso_por_id(curso_id)
    if not curso:
        print(f"Curso con ID {curso_id} no encontrado.")
        return

    dlg = ft.AlertDialog(
        title=ft.Text("Confirmar Eliminación"),
        content=ft.Text(f"¿Estás seguro de que deseas eliminar el curso '{curso['titulo']}'? Esta acción no se puede deshacer."),
        actions=[
            ft.Button("Eliminar", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: (eliminar_curso(curso_id), setattr(dlg, "open", False), cargar_vista_cursos_admin(), page.update())),
            ft.Button("Cancelar", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
        ],
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()