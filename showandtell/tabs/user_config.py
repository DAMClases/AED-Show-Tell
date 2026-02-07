import flet as ft
from database.crud import *


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
            contenido_mostrable = info_panel(datos_usuario)
            contenedor.content = ft.Column([
                ft.Row([
                ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
                ft.Divider(),
                ft.Row(contenido_mostrable, expand=True)], 
            scroll="auto")
            contenedor.update()
        case "docente":
            datos_usuario = obtener_informacion_perfil_usuario_docente(current_user["email"])
            contenido_mostrable = info_panel(datos_usuario)
            contenedor.content = ft.Column([
                ft.Row([
                ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
                ft.Divider(),
                ft.Row(contenido_mostrable, expand=True)], 
            scroll="auto")
            contenedor.update()
        case "usuario":
            datos_usuario = obtener_informacion_perfil_usuario_alumno(current_user["email"])
            contenido_mostrable = info_panel(datos_usuario)
            contenedor.content = ft.Column([
                ft.Row([
                ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
                ft.Divider(),
                ft.Row(contenido_mostrable, expand=True)], 
            scroll="auto")
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