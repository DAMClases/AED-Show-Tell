import flet as ft
from database.crud import *
from utils.elements import *


contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg


def mostrar_todos_los_alumnos(current_user:dict):
    '''Muestra todos los alumnos que tiene un docente.'''
    rows = []
    cursos = obtener_todos_los_cursos_docente(current_user["email"])
    cursos_id = [curso["curso_id"] for curso in cursos]
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
                        on_click=lambda e, a_id=informacion_alumnos[indice]['_id']:mostrar_detalles_alumno(a_id)
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

    contenedor.content = ft.Column([
        ft.Row([
            ft.Text("Información del alumnado", size=30, weight="bold"),
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    contenedor.update()

def mostrar_detalles_alumno(id_alumno):
    '''Muestra los detalles de un alumno en profundidad.'''
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
