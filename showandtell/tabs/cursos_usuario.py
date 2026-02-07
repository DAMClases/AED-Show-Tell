from datetime import datetime
import flet as ft
from database.crud import *
from utils.elements import *

contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_vista_cursos_disponibles_alumno(usuario_actual:dict):
    '''Carga la vista estilo tree de los datos de los cursos que tiene
    asociado un alumno.'''
    cursos = obtener_cursos_de_alumno(usuario_actual['email'])
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
                            on_click=lambda e, info=curso: mostrar_informacion_curso_alumno(info)
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

    contenedor.content = ft.Column([
        ft.Row([
            ft.Text("Gestión de cursos", size=30, weight="bold")], alignment="spaceBetween"),
        ft.Divider(),
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    contenedor.update()

def mostrar_informacion_curso_alumno(datos):
    '''Abre la tarjeta individual de la información de cada curso.'''
    datos_de_docente = obtener_docente_por_id(datos['instructor']['docente_id'])
    print(datos)
    profesor = ft.Text(f"Instructor: {datos['instructor']['nombre']}")
    email_instructor = ft.Text(f"Correo electrónico adjunto: {datos_de_docente['email']}")
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


