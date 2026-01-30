from datetime import datetime
import flet as ft
from database.crud import *
from utils.elements import *

content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def load_cursos_disponibles_view(current_user:dict):
    '''Carga la vista estilo tree de los datos de los cursos que tiene
    asociado un alumno.'''
    cursos = obtener_cursos_de_alumno(current_user['email'])
    print("debug de usuarios", cursos)
    id_cursos = []
    for _, valor in cursos.items():
        for val in valor:
            id_cursos.append(val['curso'])
    rows = []
    datos_cursos = obtener_datos_cursos_concretos(id_cursos)
    print(datos_cursos)
    indice = 0
    for _ in cursos:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(datos_cursos[indice]['titulo'])),
                    ft.DataCell(ft.Text(datos_cursos[indice]['descripcion'], weight="bold")),
                    ft.DataCell(ft.Text(datos_cursos[indice]['duracion_horas'], weight="bold")),
                    ft.DataCell(ft.Text(datos_cursos[indice]['precio'], weight="bold")),
                    ft.DataCell(ft.Text((None), weight="bold")),
                    ft.DataCell(ft.IconButton(ft.Icons.EDIT, on_click=None))]),
        )
        indice +=1
        
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre del curso")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Horas")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Ver más")),

        ],
        rows=rows,
        border=ft.Border(ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200")),
        heading_text_style=ft.TextStyle(weight="bold", color=ft.Colors.BLUE_GREY_900),
    )

    content_area.content = ft.Column([
        ft.Row([
            ft.Text("Gestión de cursos", size=30, weight="bold"),
            ft.Button("Añadir un curso", icon=ft.Icons.ADD,on_click=lambda e: None()) 
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    content_area.update()

#################################### Añadir un curso nuevo #################################

# def show_add_course_dialog_docente():
#     '''La modificación de este submenú es que el docente estará bloqueado y cargado previamente.'''
#     titulo = ft.TextField(label="Título del curso")
#     descripcion = ft.TextField(label="Descripción del curso", multiline=True)
#     precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
#     duracion = ft.TextField(label="Duración", keyboard_type=ft.KeyboardType.NUMBER)

#     def guardar_nuevo_curso():
#         precio_str = precio.value.replace(',', '.')
#         precio_valor = float(precio_str)
#         id_curso_correlativo = obtener_ultimo_id_curso()
#         docente_id_seleccionado = obtener_informacion_perfil_usuario_docente(page.login_data["user_email"])['_id']
#         crear_curso(
#             id = id_curso_correlativo,
#             titulo=titulo.value,
#             descripcion=descripcion.value,
#             precio=precio_valor,
#             duracion=int(duracion.value),
#             docente_id=docente_id_seleccionado,
#             docente_nombre=obtener_docente_por_id(docente_id_seleccionado)['nombre'] + " " + obtener_docente_por_id(docente_id_seleccionado)['apellidos']
#         )
#         dlg.open = False
#         #load_cursos_view()
#         page.update()

#     dlg = ft.AlertDialog(
#             title=ft.Text("Añadir nuevo curso"),
#             content=ft.Column([
#                 titulo,
#                 descripcion,
#                 precio,
#                 duracion,
#             ], tight=True),
#             actions=[
#                 ft.Button("Guardar", on_click=guardar_nuevo_curso),
#                 ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
#             ]
#         )
#     page.overlay.append(dlg)
#     dlg.open = True
#     page.update() 

# def show_add_course_dialog():
#     from utils.elements import AutocompletarCampo
#     titulo = ft.TextField(label="Título del curso")
#     descripcion = ft.TextField(label="Descripción", multiline=True)
#     precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
#     duracion = ft.TextField(label="Duración (horas)", keyboard_type=ft.KeyboardType.NUMBER)
    
#     docente_id_seleccionado = None

#     def set_docente(docente_id):
#         nonlocal docente_id_seleccionado
#         docente_id_seleccionado = docente_id
    
#     docente_id = AutocompletarCampo(set_docente, "Docente")

#     def guardar_curso(e):
#         crear_curso(
#             titulo=titulo.value,
#             descripcion=descripcion.value,
#             precio=float(precio.value),
#             duracion=int(duracion.value),
#             docente_id=docente_id_seleccionado,
#             docente_nombre=obtener_docente_por_id(docente_id_seleccionado)['nombre'] + " " + obtener_docente_por_id(docente_id_seleccionado)['apellidos']
#         )
#         dlg.open = False
#         load_cursos_view()
#         page.update()

#     dlg = ft.AlertDialog(
#         title=ft.Text("Agregar Nuevo Curso"),
#         content=ft.Column([
#             titulo,
#             descripcion,
#             precio,
#             duracion,
#             docente_id
#         ], tight=True),
#         actions=[
#             ft.Button("Guardar", on_click=guardar_curso),
#             ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
#         ]
#     )

#     page.overlay.append(dlg)
#     dlg.open = True
#     page.update()


