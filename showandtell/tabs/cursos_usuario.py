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
    id_cursos = []
    for _, valor in cursos.items():
        for val in valor:
            id_cursos.append(val['curso'])
    rows = []
    datos_cursos = obtener_datos_cursos_concretos(id_cursos)
    indice = 0
    for curso in datos_cursos:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(curso['titulo'])),
                    ft.DataCell(ft.Text(curso['descripcion'], weight="bold")),
                    ft.DataCell(ft.Text(str(curso['duracion_horas']), weight="bold")),
                    ft.DataCell(ft.Text(str(curso['precio']), weight="bold")),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.INFO_ROUNDED,
                            on_click=lambda e, info=curso: show_course_information(info)
                        )
                    ),
                ]
            )
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
            ft.Text("Gestión de cursos", size=30, weight="bold")], alignment="spaceBetween"),
        ft.Divider(),
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    content_area.update()

def show_course_information(datos):
    '''Abre la tarjeta individual de la información de cada curso.'''
    datos_de_docente = obtener_informacion_docente_curso(datos['titulo'])
    profesor = ft.Text(f"Instructor: {datos_de_docente}")
    email_instructor = ft.Text(f"Correo electrónico adjunto: {obtener_mail_docente_nombre(datos_de_docente)}")
    titulo = ft.Text(f"Título: {datos['titulo']}", size=20)
    descripcion = ft.Text(f"Descripcion: {datos['descripcion']}")
    precio = ft.Text(f"Precio: {datos['precio']}")
    duracion = ft.Text(f"Duración del curso: {datos['duracion_horas']} horas")
    dlg = ft.AlertDialog(
            title=ft.Text("Información adicional"),
            content=ft.Column([
                titulo,
                profesor,
                email_instructor,
                descripcion,
                precio,
                duracion,
            ], tight=True),
            actions=[
                ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
            ]
        )
    page.overlay.append(dlg)
    dlg.open = True
    page.update() 


