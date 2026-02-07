import flet as ft
from datetime import datetime
def mostrar_mensaje(page: ft.Page, mensaje: str, grado: str = "advertencia"):
    color = ft.Colors.BLUE_400
    mensaje_pantalla = "Información"
    icono_popup = ft.Icons.INFO
    
    match grado:
        case "advertencia":
            color = ft.Colors.ORANGE_400
            mensaje_pantalla = "¡Advertencia!"
            icono_popup = ft.Icons.WARNING
        case "error":
            color = ft.Colors.RED_400
            mensaje_pantalla = "¡Error!"
            icono_popup = ft.Icons.ERROR_OUTLINE
        case "info":
            color = ft.Colors.BLUE_400
            mensaje_pantalla = "¡Información!"
            icono_popup = ft.Icons.INFO

    def cerrar_dialogo(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(icono_popup, color=color, size=30),
                ft.Text(mensaje_pantalla, size=20, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        content=ft.Text(mensaje, size=16),
        actions=[ft.TextButton("Entendido", on_click=cerrar_dialogo)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def validar_entrada_fecha(fecha:str)->bool:
    '''Valida la entrada del campo de fecha con el formato Año-Mes-dia (Y-M-m).
   
     Luego, valida si el año es menor a 1940, que en nuestro contexto se presenta como fecha inválida.
    '''

    try:
        objeto_fecha = datetime.strptime(fecha, '%Y-%m-%d')
        if objeto_fecha.year < 1940:
            return False
        return True 
        
    except ValueError:
        return False

def validar_entrada_telefono(telefono:str)->bool:
    '''Valida la entrada numérica de un teléfono.
   
     Devuelve True solo cuando es válido en el formato estándar español de telefonía de 9 dígitos.
     '''
    if len(telefono) > 9 or len(telefono) < 9:
        return False
    elif telefono.strip().isdigit():
        return True
    return False

def validar_entrada_precio(precio:str)->bool:
    try:
        precio = float(precio)
    except ValueError:
        return False
    if precio >0:
        return True
    return False

def validar_entrada_duracion(duracion:str)->bool:
    try:
        duracion = int(duracion)
    except ValueError:
        return False
    if duracion > 0:
        return True
    return False