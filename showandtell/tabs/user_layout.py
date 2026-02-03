import flet as ft
from database.crud import *
from tabs.dashboard_user import load_dashboard_user_view
from tabs.login import login_screen
from tabs.user_config import load_usuario_view
from tabs.dashboard_user import setup as setup_dashboard
from tabs.user_config import setup as setup_usuario
from tabs.cursos_usuario import load_cursos_disponibles_view
from tabs.cursos_usuario import setup as setup_cursos

content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def build_user_layout(current_user:dict):
    setup_dashboard(content_area, page)
    setup_usuario(content_area, page)
    setup_cursos(content_area, page)

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: load_dashboard_user_view(current_user)
        elif idx == 1: load_cursos_disponibles_view(current_user)
        elif idx == 2: load_usuario_view(current_user)
        elif idx == 3: login_screen(current_user)

            # content_area.content = ft.Text("Vista     de Cursos...")
            # content_area.update()

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

    layout = ft.Row([sidebar, ft.VerticalDivider(width=1), content_area], expand=True)
    page.add(layout)
    load_dashboard_user_view(current_user)