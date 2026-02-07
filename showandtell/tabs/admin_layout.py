import flet as ft
from database.crud import *
from tabs.login import pantalla_login
from tabs.dashboard_admin import cargar_dashboard_admin, setup as setup_dashboard
from tabs.matriculas_admin import cargar_vista_matriculas_admin, setup as setup_matricula
from tabs.user_config import cargar_vista_informacion_usuario, setup as setup_usuario
from tabs.cursos_admin import cargar_vista_cursos_admin, setup as setup_cursos
from tabs.docentes_admin import cargar_vista_docentes_admin, setup as setup_docentes
from tabs.alumnos_admin import cargar_vista_alumnos_docente, setup as setup_alumnos


contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def construir_ui_admin(current_user: dict):
    
    setup_dashboard(contenedor, page)
    setup_matricula(contenedor, page)
    setup_usuario(contenedor, page)
    setup_cursos(contenedor, page)
    setup_docentes(contenedor, page)
    setup_alumnos(contenedor, page)

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: cargar_dashboard_admin()
        elif idx == 1: cargar_vista_matriculas_admin()
        elif idx == 2:cargar_vista_cursos_admin()
        elif idx == 3:cargar_vista_docentes_admin()
        elif idx == 4:cargar_vista_alumnos_docente()
        elif idx == 5:cargar_vista_informacion_usuario(current_user)
        elif idx == 6:pantalla_login(current_user)


    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type="all",
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.RECEIPT_LONG_OUTLINED, selected_icon=ft.Icons.RECEIPT_LONG, label="Matrículas"),
            ft.NavigationRailDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Cursos"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON_3, label="Docentes"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON_2, label="Alumnos"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil de usuario"),
            ft.NavigationRailDestination(icon=ft.Icons.LOGOUT, label="Cerrar sesión")
        ],
        on_change=on_nav_change
    )

    layout = ft.Row([sidebar, ft.VerticalDivider(width=1), contenedor], expand=True)
    page.add(layout)
    cargar_dashboard_admin()