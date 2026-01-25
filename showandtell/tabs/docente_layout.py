import flet as ft
from database.crud import *
from tabs.dashboard_docente import load_dashboard_docente_view, setup as setup_dashboard
from tabs.matriculas_admin import load_matricula_view, setup as setup_matricula
from tabs.login import login_screen
from tabs.user_config import load_usuario_view, setup as setup_usuario
from tabs.cursos_docente import load_cursos_disponibles_view, setup as setup_cursos


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def build_docente_layout(current_user: dict):
    '''Navegaciones del docente - carga del setup de configuración de pantalla'''
    
    setup_dashboard(content_area, page)
    setup_matricula(content_area, page)
    setup_usuario(content_area, page)
    setup_cursos(content_area, page)

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: load_dashboard_docente_view(current_user)
        elif idx == 1: load_cursos_disponibles_view(current_user)
        elif idx == 2: None
        elif idx == 3: load_usuario_view(current_user)
        elif idx == 4:login_screen(current_user)



    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type="all",
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.SCHOOL, selected_icon=ft.Icons.SCHOOL, label="Cursos"),
            ft.NavigationRailDestination(icon=ft.Icons.INFO_ROUNDED, selected_icon=ft.Icons.INFO_ROUNDED, label="Alumnos"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil de usuario"),
            ft.NavigationRailDestination(icon=ft.Icons.LOGOUT, label="Cerrar sesión")
        ],
        on_change=on_nav_change
    )

    layout = ft.Row([sidebar, ft.VerticalDivider(width=1), content_area], expand=True)
    page.add(layout)
    load_dashboard_docente_view(current_user)