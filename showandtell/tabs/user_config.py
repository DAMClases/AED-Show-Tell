import flet as ft
from database.crud import *


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def load_usuario_view(current_user: dict):
    match current_user["role"]:
        case "admin":
            datos_usuario = obtener_informacion_perfil_usuario_admin(current_user["email"])
            contenido_mostrable = info_panel(datos_usuario)
            content_area.content = ft.Column([
                ft.Row([
                ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
                ft.Divider(),
                ft.Row(contenido_mostrable, expand=True)], 
            scroll="auto")
            content_area.update()
        case "docente":
            datos_usuario = obtener_informacion_perfil_usuario_docente(current_user["email"])
            contenido_mostrable = info_panel(datos_usuario)
            content_area.content = ft.Column([
                ft.Row([
                ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
                ft.Divider(),
                ft.Row(contenido_mostrable, expand=True)], 
            scroll="auto")
            content_area.update()
        case "usuario":
            datos_usuario = obtener_informacion_perfil_usuario_docente(current_user["email"])
            contenido_mostrable = info_panel(datos_usuario)
            content_area.content = ft.Column([
                ft.Row([
                ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
                ft.Divider(),
                ft.Row(contenido_mostrable, expand=True)], 
            scroll="auto")
            content_area.update()
    
def info_panel(usuario):
    '''Vista que he construido para generar los datos del usuario.'''
    return ft.Container(
        ft.Column([
            ft.Text(f"Nombre: {usuario['nombre']}", size=14, weight="bold"),
            ft.Text(f"Apellidos: {usuario['apellidos']}", size=14, weight="bold"),
            ft.Text(f"Nombre de usuario: {usuario['email']}", size=14, weight="bold"),
            ft.Divider(),
            ft.Text(f"Teléfono: {usuario['telefono']}", size=14, color=ft.Colors.GREY_600),
            ft.Text(f"Dirección: {usuario['direccion']}", size=14, color=ft.Colors.GREY_600),
            ft.Text(f"E-mail: {usuario['email']}", size=14, color=ft.Colors.GREY_600)], spacing=10))