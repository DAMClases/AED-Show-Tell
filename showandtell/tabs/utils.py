import flet as ft

def texto_de_error(mensaje:str):
    error_dialog = ft.AlertDialog(
        modal=True, 
        title=ft.Row([
            ft.Icon(ft.icons.ERROR, color=ft.colors.RED_400, size=30),
            ft.Text("¡Error!", size=20, weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.START),
        content=ft.Text(mensaje, size=16),
        actions=[ft.TextButton("OK", on_click=lambda e: None(e))],
        actions_alignment=ft.MainAxisAlignment.END,
        title_padding=ft.Padding(20, 0, 20, 0),
        content_padding=ft.Padding(20, 10, 20, 20),
    )