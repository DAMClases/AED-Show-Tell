import flet as ft
from datetime import datetime
from database.crud import *
from tabs.login import login_screen, setup as setup_login


# --- APLICACIÓN PRINCIPAL ---

def main(page: ft.Page):
    page.title = "Panel Admin - Matrículas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    current_user = { ####
        "email": None,
        "role": None,
    }
    content_area = ft.Container(expand=True, padding=20)

    # --- Pantalla de Login ---
    
    
    setup_login(content_area, page)
    login_screen(current_user)

# Ajuste: ft.run() es el estándar actual sobre ft.app()
if __name__ == "__main__":
    ft.run(main)