import flet as ft
from database.crud import *


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def login_screen(current_user: dict):
    page.overlay.clear()
    page.clean()
    user_input = ft.TextField(label="Usuario", width=300)
    pass_input = ft.TextField(label="Contraseña", password=True, width=300)
    error_text = ft.Text("", color=ft.Colors.RED)
    
    if not hasattr(page, "login_data"):
        page.login_data = {}
    page.login_data["user_email"]= None
    page.login_data["user_role"] = None
    def login_click(e):
        resultado_login = buscar_usuario_por_email(user_input.value, pass_input.value)
        # current_user["email"] = "cristophermc@gmail.com"
        # current_user["role"] = "admin"
        # page.clean()
        # from tabs.admin_layout import build_admin_layout, setup as setup_admin
        # setup_admin(content_area, page)
        # build_admin_layout(current_user)
        if resultado_login[0]:
            from tabs.admin_layout import build_admin_layout, setup as setup_admin
            from tabs.docente_layout import build_docente_layout, setup as setup_docente
            from tabs.user_layout import build_user_layout, setup as setup_user
            page.login_data["user_email"]= user_input.value
            page.login_data["user_role"] = resultado_login[1]
            current_user["email"] = user_input.value
            current_user["role"] = resultado_login[1]
            page.clean()
            match resultado_login[1]:
                case 'usuario':
                    setup_user(content_area, page)
                    build_user_layout(current_user)
                case 'docente':
                    setup_docente(content_area, page)
                    build_docente_layout(current_user)
                case 'admin':
                    setup_admin(content_area, page)
                    build_admin_layout(current_user)
        else:
            error_text.value = "Error: Usuario/Contraseña incorrectos."
            page.update()

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=60, color=ft.Colors.BLUE),
                ft.Text("Acceso Administrativo", size=24, weight="bold"),
                user_input,
                pass_input,
                error_text,
                ft.Button("Entrar", on_click=login_click, width=300)
            ], alignment="center", horizontal_alignment="center", spacing=20),
            alignment=ft.Alignment(0, 0),
            expand=True
        )
    )