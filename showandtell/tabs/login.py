import flet as ft
from database.crud import *
from database.database_init import resetear_base_de_datos

contenedor: ft.Container
page: ft.Page

def configuracion(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def pantalla_login(current_user: dict):
    page.overlay.clear()
    page.clean()
    page.padding = 0

    user_input = ft.TextField(label="Usuario", width=300, bgcolor=ft.Colors.WHITE)
    pass_input = ft.TextField(label="Contraseña", password=True, width=300, bgcolor=ft.Colors.WHITE)
    error_text = ft.Text("", color=ft.Colors.RED)
    
    if not hasattr(page, "login_data"):
        page.login_data = {}
    page.login_data["user_email"]= None
    page.login_data["user_role"] = None
    
    def login_click(e):
        resultado_login = buscar_usuario_por_email(user_input.value, pass_input.value)
        if resultado_login[0]:
            from tabs.admin_layout import construir_ui_admin, setup as setup_admin
            from tabs.docente_layout import build_docente_layout, setup as setup_docente
            from tabs.user_layout import construir_vista_alumno, setup as setup_user
            
            page.login_data["user_email"]= user_input.value
            page.login_data["user_role"] = resultado_login[1]
            current_user["email"] = user_input.value
            current_user["role"] = resultado_login[1]
            
            page.clean()
            match resultado_login[1]:
                case 'usuario':
                    setup_user(contenedor, page)
                    construir_vista_alumno(current_user)
                case 'docente':
                    setup_docente(contenedor, page)
                    build_docente_layout(current_user)
                case 'admin':
                    setup_admin(contenedor, page)
                    construir_ui_admin(current_user)
        else:
            error_text.value = "Error: Usuario/Contraseña incorrectos."
            page.update()
    def mostrar_resetear_base_datos(e):
        # Mostrar mensaje de confirmación antes de resetear la base de datos
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar acción"),
            content=ft.Text("¿Estás seguro de que deseas resetear/crear la base de datos? Esta acción eliminará todos los datos actuales."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dlg)),
                ft.ElevatedButton("Confirmar", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=lambda e: resetear_base_de_datos(page))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def cerrar_dialog(dlg):
        dlg.open = False
        page.update()


    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="../assets/background_login.png",
                    fit="cover", 
                    width=float("inf"),
                    height=float("inf"), 
                    opacity=0.9
                ),
               
                ft.Container(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.CAST_FOR_EDUCATION, size=60, color=ft.Colors.BLUE),
                            ft.Text("Iniciar sesión", size=24, weight="bold", color=ft.Colors.BLACK),
                            user_input,
                            pass_input,
                            error_text,
                            ft.ElevatedButton("Iniciar sesión", on_click=login_click, width=300, icon=ft.Icons.LOGIN),
                            
                            ft.ElevatedButton("Resetear/Crear base de datos", on_click=lambda e: mostrar_resetear_base_datos(page), width=300, icon=ft.Icons.RESTART_ALT)
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                        
                        bgcolor=ft.Colors.WHITE,
                        padding=40,
                        border_radius=15,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK))
                    ),
                    alignment=ft.Alignment(0, 0), 
                )
            ],
            expand=True 
        )
    )