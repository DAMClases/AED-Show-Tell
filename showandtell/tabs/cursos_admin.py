import flet as ft
from database.crud import *
from utils.elements import *


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def load_cursos_view():
    
    datos_cursos = obtener_datos_cursos()
    from utils.elements import CursoCard
    course_cards = [CursoCard(page,curso) for curso in datos_cursos]
    content_area.content = ft.Column([
        ft.Row([
        ft.Text("Gestión de Cursos", size=30, weight="bold"),
        ft.Button("Agregar Nuevo Curso", icon=ft.Icons.ADD, on_click=lambda e: mostrar_añadir_curso_dialog())
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Row(course_cards, wrap=True, spacing=20, run_spacing=20)
    ], scroll="auto")
    content_area.update()

def mostrar_añadir_curso_dialog():
    from utils.elements import AutocompletarCampo
    titulo = ft.TextField(label="Título del curso")
    descripcion = ft.TextField(label="Descripción", multiline=True)
    precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
    duracion = ft.TextField(label="Duración (horas)", keyboard_type=ft.KeyboardType.NUMBER)
    
    docente_id_seleccionado = None

    def set_docente(docente_id):
        nonlocal docente_id_seleccionado
        docente_id_seleccionado = docente_id
    
    docente_id = AutocompletarCampo(set_docente, "Docente")

    def guardar_curso(e):
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
        dlg.open = False
        load_cursos_view()
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

def mostrar_editar_curso_dialog(curso):
    from utils.elements import AutocompletarCampo
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

    docente_id = AutocompletarCampo(set_docente, "Docente", curso['instructor']['nombre'])

    docente_id_seleccionado = curso['instructor']['docente_id']

    def editar_curso_info(e):
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
        dlg.open = False
        load_cursos_view()
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
            ft.Button("Actualizar", on_click=editar_curso_info),
            ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
        ]
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def show_course_details(curso_id):
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
            ft.Button("Editar", icon=ft.Icons.EDIT, on_click=lambda e: mostrar_editar_curso_dialog(curso)),
            ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
        ],
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()