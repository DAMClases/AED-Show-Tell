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

def load_docentes_view():
    rows = []
    docentes = obtener_docentes()
    
    for docente in docentes:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(docente["nombre"], weight="bold")),
                    ft.DataCell(ft.Text(docente["apellidos"], weight="bold")),
                    ft.DataCell(ft.Text(docente["telefono"])),
                    ft.DataCell(ft.Text(docente["email"])),
                    ft.DataCell(ft.Text(docente["direccion"])),
                    ft.DataCell(ft.Text(docente["estado"])),
                    ft.DataCell(ft.Text(docente["fecha_alta"])),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.EDIT,
                            on_click=lambda e, d_id=docente["_id"]: 
                                mostrar_detalles_docente(d_id)
                        )
                    ),
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Fecha de alta")),            
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=rows,
        border=ft.Border(ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200")),
        heading_text_style=ft.TextStyle(weight="bold", color=ft.Colors.BLUE_GREY_900),
    )

    content_area.content = ft.Column([
        ft.Row([
            ft.Text("Gestión de Docentes", size=30, weight="bold"),
            ft.Button("Agregar Docente", icon=ft.Icons.ADD,on_click=lambda e: show_add_docente_dialog()) 
        ], alignment="spaceBetween"),
        ft.Divider(),
        table
    ], scroll="auto")
    content_area.update()

def show_add_docente_dialog():
    nombre = ft.TextField(label="Nombre")
    email = ft.TextField(label="Email")
    telefono = ft.TextField(label="Teléfono")
    especialidad = ft.TextField(label="Especialidad")

    def guardar_docente(e):
        crear_docente(
            nombre=nombre.value,
            email=email.value,
            telefono=telefono.value,
            especialidad=especialidad.value
        )
        dlg.open = False
        load_docentes_view()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Agregar Nuevo Docente"),
        content=ft.Column([
            nombre,
            email,
            telefono,
            especialidad
        ]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dlg)),
            ft.ElevatedButton("Guardar", on_click=guardar_docente)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dlg
    dlg.open = True
    page.update()

def cerrar_dialog(dialog):
    dialog.open = False
    page.update()

def mostrar_detalles_docente(docente_id):
    docente = obtener_docente_por_id(docente_id)
    dlg = ft.AlertDialog(
        title = ft.Text(f"Detalle de Docente: {docente['nombre']} {docente['apellidos']}"),
        content = ft.Column([
            ft.Text(f"Nombre: {docente['nombre']}"),
            ft.Text(f"Apellidos: {docente['apellidos']}"),
            ft.Text(f"Teléfono: {docente['telefono']}"),
            ft.Text(f"Email: {docente['email']}"),
            ft.Text(f"Dirección: {docente['direccion']}"),
            ft.Text(f"Estado: {docente['estado']}"),
            ft.Text(f"Fecha de alta: {docente['fecha_alta']}"),
            ft.Text(f"Contraseña: {"*" * len(docente['password'])}")
        ], spacing=10),
        actions=[
            ft.Button("Editar", icon=ft.Icons.EDIT, on_click=lambda e: show_edit_docente_dialog(docente_id)),
            ft.Button("Cerrar", on_click=lambda e: cerrar_dialog(dlg))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def show_edit_docente_dialog(docente_id):
    docente = obtener_docente_por_id(docente_id)
    nombre = ft.TextField(label="Nombre", value=docente["nombre"])
    apellidos = ft.TextField(label="Apellidos", value=docente["apellidos"])
    telefono = ft.TextField(label="Teléfono", value=docente["telefono"])
    email = ft.TextField(label="Email", value=docente["email"])
    direccion = ft.TextField(label="Dirección", value=docente["direccion"])
    estado = ft.TextField(label="Estado", value=docente["estado"])
    fecha_altsa = ft.TextField(label="Fecha de alta", value=docente["fecha_alta"])
    password = ft.TextField(label="Contraseña", value=docente["password"], password=True)

    def guardar_cambios(e):
        actualizar_docente(
            docente_id,
            nombre=nombre.value,
            apellidos=apellidos.value,
            telefono=telefono.value,
            email=email.value,
            direccion=direccion.value,
            estado=estado.value,
            fecha_alta=fecha_altsa.value,
            password=password.value
        )
        dlg.open = False
        load_docentes_view()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Editar Docente"),
        content=ft.Column([
            nombre,
            apellidos,
            telefono,
            email,
            direccion,
            estado,
            fecha_altsa,
            password
        ]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dlg)),
            ft.ElevatedButton("Guardar Cambios", on_click=guardar_cambios)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()