import flet as ft
from database.crud import *
from tabs.dashboard_user import cargar_dashboard_alumno
from tabs.login import pantalla_login
from tabs.user_config import cargar_vista_informacion_usuario
from tabs.dashboard_user import setup as setup_dashboard
from tabs.user_config import setup as setup_usuario
from tabs.cursos_usuario import cargar_vista_cursos_disponibles_alumno
from tabs.cursos_usuario import setup as setup_cursos

contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def construir_vista_alumno(current_user:dict):
    setup_dashboard(contenedor, page)
    setup_usuario(contenedor, page)
    setup_cursos(contenedor, page)

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: cargar_dashboard_alumno(current_user)
        elif idx == 1: cargar_vista_cursos_disponibles_alumno(current_user)
        elif idx == 2: cargar_vista_informacion_usuario(current_user)
        elif idx == 3: pantalla_login(current_user)

            # contenedor.content = ft.Text("Vista     de Cursos...")
            # contenedor.update()

    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type="all",
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Cursos"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil de usuario"),
            ft.NavigationRailDestination(icon=ft.Icons.LOGOUT, label="Cerrar sesión")
        ],
        on_change=on_nav_change
    )

    layout = ft.Row([sidebar, ft.VerticalDivider(width=1), contenedor], expand=True)
    page.add(layout)
    cargar_dashboard_alumno(current_user)