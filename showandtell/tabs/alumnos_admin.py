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

def cargar_vista_alumnos_docente():
    rows = []
    alumnos = obtener_todos_los_alumnos()
    
    for alumno in alumnos:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(alumno["nombre"], weight="bold")),
                    ft.DataCell(ft.Text(alumno["apellidos"], weight="bold")),
                    ft.DataCell(ft.Text(alumno["telefono"])),
                    ft.DataCell(ft.Text(alumno["email"])),
                    ft.DataCell(ft.Text(alumno["direccion"])),
                    ft.DataCell(ft.Text(alumno["estado"])),
                    ft.DataCell(ft.Text(alumno["fecha_alta"])),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.EDIT,
                            on_click=lambda e, a_id=alumno["_id"]: 
                                mostrar_detalles_alumno(a_id)
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

    contenedor.content = ft.Column([
        ft.Row([
            ft.Text("Gestión de Alumnos", size=30, weight="bold"),
            ft.Button("Agregar Alumno", icon=ft.Icons.ADD,on_click=lambda e: mostrar_popup_añadir_alumno()) 
        ], alignment="spaceBetween"),
        ft.Divider(),
        table
    ], scroll="auto")
    contenedor.update()

def mostrar_popup_añadir_alumno():
    nombre = ft.TextField(label="Nombre")
    apellidos = ft.TextField(label="Apellidos")
    telefono = ft.TextField(label="Teléfono")
    email = ft.TextField(label="Email")
    direccion = ft.TextField(label="Dirección")
    estado = ft.TextField(label="Estado")
    fecha_alta = ft.TextField(label="Fecha de alta")
    password = ft.TextField(label="Contraseña", password=True)

    def guardar_alumno(e):
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
        registrar_nuevo_alumno(datos)
        dlg.open = False
        cargar_vista_alumnos_docente()
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Agregar Nuevo Alumno"),
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
            ft.ElevatedButton("Guardar", on_click=guardar_alumno)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def cerrar_dialog(dialog):
    dialog.open = False
    page.update()

def mostrar_detalles_alumno(alumno_id):
    alumno = obtener_alumno_por_id(alumno_id)
    dlg = ft.AlertDialog(
        title = ft.Text(f"Detalle de Alumno: {alumno['nombre']} {alumno['apellidos']}"),
        content = ft.Column([
        ft.Text(f"Nombre {alumno['nombre']}"),
        ft.Text(f"Apellidos {alumno['apellidos']}"),
        ft.Text(f"Teléfono {alumno['telefono']}"),
        ft.Text(f"Email {alumno['email']}"),
        ft.Text(f"Dirección {alumno['direccion']}"),
        ft.Text(f"Estado {alumno['estado']}"),
        ft.Text(f"Fecha de alta {alumno['fecha_alta']}"),
        ft.Text(f"Contraseña {'*' * len(alumno['password'])}")
        ], spacing=10),
        actions=[
            ft.Button("Editar", icon=ft.Icons.EDIT, on_click=lambda e: mostrar_editar_alumno_dialog(alumno_id)),
            ft.Button("Borrar", icon=ft.Icons.DELETE, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: (mostrar_confirmacion_eliminar_alumno(alumno_id), setattr(dlg, "open", False), page.update())),
            ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
        ],
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()


def mostrar_editar_alumno_dialog(alumno_id):
    alumno = obtener_alumno_por_id(alumno_id)
    nombre = ft.TextField(label="Nombre", value=alumno["nombre"])
    apellidos = ft.TextField(label="Apellidos", value=alumno["apellidos"])
    telefono = ft.TextField(label="Teléfono", value=alumno["telefono"])
    email = ft.TextField(label="Email", value=alumno["email"])
    direccion = ft.TextField(label="Dirección", value=alumno["direccion"])
    estado = ft.TextField(label="Estado", value=alumno["estado"])
    fecha_alta = ft.TextField(label="Fecha de alta", value=alumno["fecha_alta"])
    password = ft.TextField(label="Contraseña", value=alumno["password"], password=True)
    def guardar_cambios(e):
            actualizar_alumno(
                alumno_id,
                nombre=nombre.value,
                apellidos=apellidos.value,
                telefono=telefono.value,
                email=email.value,
                direccion=direccion.value,
                estado=estado.value,
                fecha_alta=fecha_alta.value,
                password=password.value
            )
            dlg.open = False
            cargar_vista_alumnos_docente()
            page.update()

    dlg = ft.AlertDialog(
        title = ft.Text(f"Detalle de Alumno: {alumno['nombre']} {alumno['apellidos']}"),
        content = ft.Column([
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
            ft.Button("Guardar", on_click=guardar_cambios),
            ft.Button("CERRAR", on_click=lambda _: cerrar_dialog(dlg))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

    
def mostrar_confirmacion_eliminar_alumno(alumno_id):
    dlg = ft.AlertDialog(
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este alumno? Esta acción no se puede deshacer."),
        actions=[
            ft.Button("Cancelar", on_click=lambda e: cerrar_dialog(dlg)),
            ft.Button("Eliminar", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: (eliminar_alumno(alumno_id), cerrar_dialog(dlg), cargar_vista_alumnos_docente()))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()