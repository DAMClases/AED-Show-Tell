import flet as ft
from datetime import datetime
from database.crud import *
from tabs.login import pantalla_login, configuracion as setup_login


# --- APLICACIÓN PRINCIPAL ---

def main(page: ft.Page):
    init_db(MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)["academia"])
    page.title = "Show & Tell"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    current_user = { ####
        "email": None,
        "role": None,
    }
    content_area = ft.Container(expand=True, padding=20)

    # --- Pantalla de Login ---
    
    
    setup_login(content_area, page)
    pantalla_login(current_user)

if __name__ == "__main__":
    ft.run(main)