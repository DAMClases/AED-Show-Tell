import flet as ft
from database.crud import *
from showandtell.tabs.dashboard_admin import load_dashboard_view


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def build_user_layout():
    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: load_dashboard_view()
        elif idx == 1:
            content_area.content = ft.Text("Vista de Cursos...")
            content_area.update()

    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type="all",
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Cursos"),
        ],
        on_change=on_nav_change
    )

    layout = ft.Row([sidebar, ft.VerticalDivider(width=1), content_area], expand=True)
    page.add(layout)
    load_dashboard_view()