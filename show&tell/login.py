import flet as ft

def main(page: ft.Page):
    page.title = "Iniciar sesión"
    page.add(ft.TextField(hint_text="Nombre de usuario", width=300))
    page.add(ft.TextField(hint_text="Contraseña", width=300))

    page.update()

if __name__ == '__main__':
    ft.app(target=main)
