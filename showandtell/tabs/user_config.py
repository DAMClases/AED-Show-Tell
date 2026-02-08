import flet as ft
from database.crud import *
from showandtell.utils.validaciones import mostrar_mensaje


contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_vista_informacion_usuario(current_user: dict):
    match current_user["role"]:
        case "admin":
            datos_usuario = obtener_informacion_perfil_usuario_admin(current_user["email"])
        case "docente":
            datos_usuario = obtener_informacion_perfil_usuario_docente(current_user["email"])
        case "usuario":
            datos_usuario = obtener_informacion_perfil_usuario_alumno(current_user["email"])
    contenido_mostrable = info_panel(datos_usuario)
    contenedor.content = ft.Column([
        ft.Row([
            ft.Text("Información de la cuenta", size=30, weight="bold")
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Row([contenido_mostrable], expand=True),
        ft.Divider(),
        ft.Button("Cambiar contraseña", on_click=lambda e: mostrar_popup_cambiar_contraseña(current_user))
    ], expand=True, scroll="auto")
    contenedor.update()
    
def info_panel(usuario):
    '''Vista que muestra los datos del usuario.'''
    return ft.Container(
        ft.Column([
            ft.Text(f"Nombre: {usuario['nombre']}", size=14, weight="bold"),
            ft.Text(f"Apellidos: {usuario['apellidos']}", size=14, weight="bold"),
            ft.Text(f"Nombre de usuario: {usuario['email']}", size=14, weight="bold"),
            ft.Divider(),
            ft.Text(f"Teléfono: {usuario['telefono']}", size=14, color=ft.Colors.GREY_600),
            ft.Text(f"Dirección: {usuario['direccion']}", size=14, color=ft.Colors.GREY_600),
            ft.Text(f"E-mail: {usuario['email']}", size=14, color=ft.Colors.GREY_600)], spacing=10))

def mostrar_popup_cambiar_contraseña(current_user):
    '''Muestra un popup para cambiar la contraseña del usuario.'''
    new_password = ft.TextField(label="Nueva contraseña", password=True)
    confirm_password = ft.TextField(label="Confirmar contraseña", password=True)
    def cambiar_contraseña(dialog):
        if new_password.value != confirm_password.value:
            mostrar_mensaje(page, "Las contraseñas no coinciden.", "error")
            return
        if len(new_password.value) < 6:
            mostrar_mensaje(page, "La contraseña debe tener al menos 6 caracteres.", "error")
            return
        actualizar_contraseña(current_user["email"], new_password.value, current_user["role"])
        mostrar_mensaje(page, "Contraseña actualizada correctamente.", "info")
        dialog.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Cambiar contraseña"),
        content=ft.Column([new_password, confirm_password], spacing=10),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False)),
            ft.ElevatedButton("Cambiar", on_click=lambda e: cambiar_contraseña(dlg))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: None
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()