import flet as ft
from database.crud import *
from tabs.cursos_admin import mostrar_detalles_curso

# --- Componentes de UI Reutilizables ---

def StatusBadge(status):
    """Crea una etiqueta de color según el estado"""
    colors = {
        "pagado": ft.Colors.GREEN_400,
        "pendiente": ft.Colors.ORANGE_400,
        "cancelado": ft.Colors.RED_400,
    }
    color = colors.get(status, ft.Colors.GREY_400)
    return ft.Container(
        content=ft.Text(status, color=ft.Colors.WHITE, size=12, weight="bold"),
        bgcolor=color,
        # Ajuste: Uso de clase Padding y BorderRadius para evitar advertencias
        padding=ft.Padding(10, 5, 10, 5),
        border_radius=ft.BorderRadius(15, 15, 15, 15),
        alignment=ft.Alignment(0, 0)
    )

def MetricCard(title, value, icon, color):
    """Tarjeta pequeña para el Dashboard"""
    return ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Row([
                ft.Icon(icon, color=color, size=40),
                ft.Column([
                    ft.Text(title, size=14, color=ft.Colors.GREY_500),
                    ft.Text(str(value), size=24, weight="bold")
                ], spacing=5)
            ], alignment="spaceBetween") # Ajuste: String para evitar problemas de atributo
        )
    )

# Autocompletar
def AutocompletarCampo(on_select, campo:str, valor_inicial=None):
    match campo:
        case "Curso":
            datos = obtener_datos_cursos()
        case "Docente":
            datos = obtener_docentes()
        case "Alumno":
            datos = obtener_todos_los_alumnos()


    input = ft.TextField(label=campo,
                            on_change=lambda e: on_change(e),
    )
    if valor_inicial:
        input.value = valor_inicial

    list_view = ft.ListView(
        height=220,
        spacing=5
    )

    dropdown = ft.Container(
        content=list_view,
        bgcolor=ft.Colors.SURFACE,
        border=ft.Border.all(1, ft.Colors.OUTLINE),
        border_radius=6,
        padding=5,
        visible=False,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
        ),
    )


    def on_change(e):
        texto = input.value.lower().strip()
        list_view.controls.clear()

        if not texto:
            dropdown.visible = False
            input.page.update()
            return

        
        for dato in datos:
            match campo:
                case "Curso":
                    texto_busqueda = dato["titulo"]
                case "Docente":
                    texto_busqueda = f"{dato['nombre']} {dato['apellidos']}"
                case "Alumno":
                    texto_busqueda = f"{dato['nombre']} {dato['apellidos']}"
            if texto in texto_busqueda.lower():
                list_view.controls.append(
                    ft.ListTile(
                        title=ft.Text(texto_busqueda),
                        on_click=lambda e, c=dato: select(c)
                    )
                )

        dropdown.visible = len(list_view.controls) > 0
        input.page.update()

    def select(dato):
        input.value = dato["titulo"] if campo=="Curso" else f"{dato['nombre']} {dato['apellidos']}"
        input.data = dato["_id"]
        dropdown.visible = False
        input.page.update()
        on_select(dato["_id"])

    return ft.Column(
        [
            input,
            dropdown,
        ],
        spacing=2,
    )


def CursoCard(page, curso):
    """Tarjeta para mostrar información del curso"""
    return ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text(curso['titulo'], size=18, weight="bold"),
                ft.Text(f"Precio: ${curso['precio']:.2f}", size=14, color=ft.Colors.GREY_600),
                ft.Text(f"Duración: {curso['duracion_horas']} horas", size=14, color=ft.Colors.GREY_600),
                ft.Text(f"Instructor: {curso['instructor']['nombre']}", size=14, color=ft.Colors.GREY_600),
                ft.Button("Ver Detalles", bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE, on_click=lambda e, c_id=curso['_id']: mostrar_detalles_curso(c_id))
            ], spacing=10)
        )
    )

import flet as ft

def mostrar_mensaje(page: ft.Page, mensaje: str, grado: str = "advertencia"):    
    '''Componente reutilizable para generar un texto de error/advertencia'''
    
    color = ft.Colors.BLUE_400
    mensaje_pantalla = "Información"
    icono_popup = "info"

    match grado:
        case 'advertencia':
            color = ft.Colors.ORANGE_400
            mensaje_pantalla = "¡Advertencia!"
            print("entre por aqui")
            icono_popup = "warning"
        
        case 'error':
            color = ft.Colors.RED_400
            mensaje_pantalla = "¡Error!"
            print("entre por aqui")
            icono_popup = "error_outline"

        case 'info':
            color = ft.Colors.BLUE_400
            mensaje_pantalla = "¡Información!"
            icono_popup = "info"

    def cerrar_dialogo(e):
        page.close(error_dialog)

    error_dialog = ft.AlertDialog(
        modal=True, 
        title=ft.Row([
            ft.Icon(icono_popup, color=color, size=30),
            ft.Text(mensaje_pantalla, size=20, weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        content=ft.Text(mensaje, size=16),
        actions=[
            ft.TextButton("Entendido", on_click=cerrar_dialogo)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        title_padding=ft.Padding(20, 20, 20, 10),
        content_padding=ft.Padding(20, 0, 20, 20),
    )

    page.open(error_dialog)