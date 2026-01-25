import flet as ft
from database.crud import *
from utils.elements import *


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg


def show_all_alumnos(current_user:dict):
    rows = []
    cursos = obtener_todos_los_cursos_docente(current_user["email"])
    cursos_id = [curso["curso_id"] for curso in cursos]
    print(cursos_id)
    informacion_alumnos = obtener_alumnos_de_un_curso(cursos_id)
    datos_curso_lista = obtener_informacion_curso(cursos_id)
    indice = 0
    for _ in informacion_alumnos:
        titulo = obtener_titulo_curso(informacion_alumnos[indice]['curso_filtrado'])
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(informacion_alumnos[indice]['_id'])),
                    ft.DataCell(ft.Text(informacion_alumnos[indice]['nombre'], weight="bold")),
                    ft.DataCell(ft.Text(informacion_alumnos[indice]['apellidos'], weight="bold")),
                    ft.DataCell(ft.Text(titulo, weight="bold")),
                    ft.DataCell(
                    ft.IconButton(
                        ft.Icons.BADGE_OUTLINED,
                        on_click=lambda e, a_id=informacion_alumnos[indice]['_id']:show_alumno_details(a_id)
                    )
                ),
                ]
            )
        )
        indice +=1
        
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Ver ficha")),

        ],
        rows=rows,
        border=ft.Border(ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200")),
        heading_text_style=ft.TextStyle(weight="bold", color=ft.Colors.BLUE_GREY_900),
    )

    content_area.content = ft.Column([
        ft.Row([
            ft.Text("Información del alumnado", size=30, weight="bold"),
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    content_area.update()

def show_alumno_details(id_alumno):
    informacion_alumno = obtener_informacion_alumno(id_alumno)
    dlg = ft.AlertDialog(
        title=ft.Text(f"Ficha del alumno: {informacion_alumno['apellidos']}, {informacion_alumno['nombre']}"),
        content=ft.Column([
            ft.Text(f"ID: {informacion_alumno['_id']}"),
            ft.Text(f"Nombre: {informacion_alumno['nombre']}"),
            ft.Text(f"Apellidos: {informacion_alumno['apellidos']}"),
            ft.Text(f"Dirección: {informacion_alumno['direccion']}"),
            ft.Text(f"Estado: {informacion_alumno['estado']}"),
            ft.Text(f"Fecha de alta: {informacion_alumno['fecha_alta']}"),
            ft.Divider(),
            ft.Text("Información de contacto",size=30, weight="bold"),
            ft.Text(f"Email: {informacion_alumno['email']}"),
            ft.Text(f"Teléfono personal: {informacion_alumno['telefono']}"),
            ft.Text(f"Teléfono fijo: {informacion_alumno['telefono_fijo']}"),
        ], spacing=10),
        actions=[
            ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
        ],
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()
# def show_course_details(curso_id):
#     curso = obtener_curso_por_id(curso_id)
#     if not curso:
#         print(f"Curso con ID {curso_id} no encontrado.")
#         return

#     dlg = ft.AlertDialog(
#         title=ft.Text(f"Detalles del Curso: {curso['titulo']}"),
#         content=ft.Column([
#             ft.Text(f"ID: {curso['_id']}"),
#             ft.Text(f"Descripción: {curso['descripcion']}"),
#             ft.Text(f"Precio: ${curso['precio']:.2f}"),
#             ft.Text(f"Duración: {curso['duracion_horas']} horas"),
#             ft.Text(f"Instructor: {curso['instructor']['nombre']}"),
#         ], spacing=10),
#         actions=[
#             ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
#         ],
#     )

#     page.overlay.append(dlg)
#     dlg.open = True
#     page.update()