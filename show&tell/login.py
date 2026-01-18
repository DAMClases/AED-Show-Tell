import flet as ft
from .database.controller import *

async def main(page: ft.Page):
    # --- CONFIGURACIÓN DE VENTANA BÁSICA PARA EL LOGIN ---
    # --- This page provides screen settings for the view ---
    page.window.width = 600
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False
    await page.window.center()
    
    page.title = "Show & Tell"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    def validar_login(e):
        username = campo_usuario.value
        passwd = campo_passwd.value

        if not username and not passwd:
            campo_usuario.error = "Campo obligatorio"            
            campo_passwd.error = "Campo obligatorio"
            return
        elif username and not passwd:
            campo_usuario.error = None
            campo_passwd.error = "Campo obligatorio"

        elif passwd and not username:
            campo_usuario.error = "Campo obligatorio"
            campo_passwd.error = None
        else:
            campo_usuario.error = None
            campo_passwd.error = None
            print(f"Usuario: {campo_usuario.value} | Pass: {campo_passwd.value}")
        page.update()

    # --- CAMPOS ---
    # --- MAIN FIELDS ---
    campo_usuario = ft.TextField(
        label="Usuario", 
        width=240, 
        height=70, 
        bgcolor=ft.Colors.WHITE, 
        color=ft.Colors.BLACK,
        border_color=ft.Colors.BLACK_87,
        content_padding=10,
        text_size=14,
        max_length=20,
        error=None
    )
    
    campo_passwd = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True,
        width=240, 
        height=70, 
        bgcolor=ft.Colors.WHITE, 
        color=ft.Colors.BLACK,
        border_color=ft.Colors.BLACK_87,
        content_padding=10,
        text_size=14,
        max_length=20,
        error=None
    )
    #--- DISPARADOR DE EVENTO ---
    #--- EVENT TRIGGER ---

    boton_entrar = ft.Button(
        "Entrar", 
        width=240,
        height=40, 
        bgcolor=ft.Colors.DEEP_PURPLE_500, 
        color=ft.Colors.WHITE, 
        on_click=validar_login,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )
    #--- CONTAINER ---
    tarjeta_login = ft.Container(
        content=ft.Column(
            [
                ft.Text("Bienvenido", size=24, weight="bold", color=ft.Colors.BLACK87),
                ft.Text("Show & Tell", size=16, color=ft.Colors.GREY_700, height=20),
                ft.Divider(height=20, color="transparent"),
                campo_usuario,
                campo_passwd,
                ft.Divider(height=10, color="transparent"),
                boton_entrar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=320,
        padding=40,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=20, 
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            offset=ft.Offset(0, 10)
        ),
    )

    
    ############# ORGANIZACIÓN COMPLETA EN UN SOLO LAYOUT ###############
    ############# THE WHOLE INFORMATION ORGANIZED IN A SINGLE LAYOUT #############
    
    layout_principal = ft.Stack(
    [
        ft.Container(
            image=ft.DecorationImage(
                src="background_login.png",
                fit="cover",
            ),
            expand=True,
        ),
        ft.Container(
            content=tarjeta_login,
            alignment=ft.Alignment.CENTER,
        ),
    ],
    expand=True,
)

    page.add(layout_principal)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")