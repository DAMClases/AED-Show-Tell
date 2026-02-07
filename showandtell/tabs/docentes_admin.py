from datetime import datetime
import flet as ft
from database.crud import *
from utils.elements import *
from utils.validaciones import *

content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def cargar_vista_docentes_admin():
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
            ft.Button("Agregar Docente", icon=ft.Icons.ADD,on_click=lambda e: mostrar_popup_añadir_docente()) 
        ], alignment="spaceBetween"),
        ft.Divider(),
        table
    ], scroll="auto")
    content_area.update()

def mostrar_popup_añadir_docente():
    nombre = ft.TextField(label="Nombre")
    apellidos = ft.TextField(label="Apellidos")
    telefono = ft.TextField(label="Teléfono")
    email = ft.TextField(label="Email")
    direccion = ft.TextField(label="Dirección")
    estado = ft.TextField(label="Estado")
    fecha_alta = ft.TextField(label="Fecha de alta")
    password = ft.TextField(label="Contraseña", password=True)

    def guardar_docente(e):
        datos = {
            "nombre": nombre.value,
            "apellidos": apellidos.value,
            "telefono": telefono.value,
            "email": email.value,
            "direccion": direccion.value,
            "estado": estado.value,
            "fecha_alta": fecha_alta.value,
            "password": password.value
        }
        if not datos["nombre"] or not datos["apellidos"] or not datos["telefono"] or not datos["email"] or not datos["direccion"] or not datos["estado"] or not datos["fecha_alta"] or not datos["password"]:
            mostrar_mensaje(page, "Alguno de los campos se encuentran vacíos. Por favor, rellénelos previamente antes de continuar.", "advertencia")
            return
        if not validar_entrada_telefono(datos["telefono"]):
            mostrar_mensaje(page, "Formato de teléfono inválido. El teléfono introducido debe tener 9 dígitos enteros.")
            return
        if not validar_entrada_fecha(datos["fecha_alta"]):
            mostrar_mensaje(page, "Formato de fecha inválido. La fecha introducida debe estar en el formato Año-Mes-día y el año de nacimiento debe ser mayor o igual a 1940.")
            return

        crear_docente(datos)
        dlg.open = False
        cargar_vista_docentes_admin()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Agregar Nuevo Docente"),
        content=ft.Column([
            nombre,
            apellidos,
            telefono,
            email,
            direccion,
            estado,
            fecha_alta,
            password
        ]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dlg)),
            ft.ElevatedButton("Guardar", on_click=guardar_docente)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
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
            ft.Text(f"Contraseña: {'*' * len(docente['password'])}")
        ], spacing=10),
        actions=[
            ft.Button("Editar", icon=ft.Icons.EDIT, on_click=lambda e: mostrar_editar_docente_dialog(docente_id)),
            ft.Button("Borrar", icon=ft.Icons.DELETE, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: (mostrar_confirmacion_eliminar_docente(docente_id), setattr(dlg, "open", False), page.update())),
            ft.Button("Cerrar", on_click=lambda e: cerrar_dialog(dlg))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def mostrar_editar_docente_dialog(docente_id):
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
        if not nombre.value or not apellidos.value or not telefono.value or not email.value or not estado.value or not fecha_altsa.value or not password.value:
            mostrar_mensaje(page, "Alguno de los campos se encuentran vacíos. Por favor, rellénelos previamente antes de continuar.", "advertencia")
            return
        if not validar_entrada_telefono(telefono.value):
            mostrar_mensaje(page, "Formato de teléfono inválido. El teléfono introducido debe tener 9 dígitos enteros.")
            return
        if not validar_entrada_fecha(fecha_altsa.value):
            mostrar_mensaje(page, "Formato de fecha inválido. La fecha introducida debe estar en el formato Año-Mes-día y el año de nacimiento debe ser mayor o igual a 1940.")
            return
        
            ########################################################
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
        mostrar_mensaje(page, "Nuevo curso implementado correctamente en el sistema.", "info")
        dlg.open = False
        cargar_vista_docentes_admin()
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

def mostrar_confirmacion_eliminar_docente(docente_id):
    def eliminar(e):
        eliminar_docente(docente_id)
        dlg.open = False
        cargar_vista_docentes_admin()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Confirmar Eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este docente? Esta acción no se puede deshacer."),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dlg)),
            ft.ElevatedButton("Eliminar", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=eliminar)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()