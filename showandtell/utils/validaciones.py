import flet as ft
from datetime import datetime
import re
from database.crud import comprobar_email_unico

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

def validar_entrada_email(email:str)->bool:
    '''Valida la entrada de un email.
   
     Devuelve True solo cuando es válido en el formato estándar de correo electrónico.
     '''
    patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(patron_email, email):
        return True
    return False

def validar_datos(datos: dict, page) -> bool:
    '''Valida que los datos de un formulario no estén vacíos y cumplan con los formatos esperados.
    
    Devuelve True solo si todos los campos requeridos están presentes, no están vacíos y cumplen con los formatos específicos (como email, teléfono, fecha, etc.).
    '''
    
    if not all(datos.values()):
        mostrar_mensaje(page, "Todos los campos son obligatorios. Por favor, rellénelos antes de continuar.", "advertencia")
        return False
    for campo, valor in datos.items():
        if not valor.strip():
            mostrar_mensaje(page, f"El campo '{campo}' no puede estar vacío. Por favor, rellénelo antes de continuar.", "advertencia")
            return False
        if campo == "email" and not validar_entrada_email(valor):
            mostrar_mensaje(page, f"El campo '{campo}' tiene un formato de email inválido.", "advertencia")
            return False
        if campo == "email" and not comprobar_email_unico(valor):
            mostrar_mensaje(page, f"El email '{valor}' ya existe en el sistema. Por favor, ingrese un email diferente.", "advertencia")
            return False
        if campo == "telefono" and not validar_entrada_telefono(valor):
            mostrar_mensaje(page, f"El campo '{campo}' tiene un formato de teléfono inválido. Debe contener exactamente 9 dígitos numéricos.", "advertencia")
            return False
        if campo == "fecha_alta" and not validar_entrada_fecha(valor):
            mostrar_mensaje(page, f"El campo '{campo}' tiene un formato de fecha inválido. Debe tener el formato Año-Mes-Día (YYYY-MM-DD) y ser posterior a 1940.", "advertencia")
            return False
        if campo == "precio" and not validar_entrada_precio(valor):
            mostrar_mensaje(page, f"El campo '{campo}' tiene un formato de precio inválido. Debe ser un número mayor que 0.", "advertencia")
            return False
        if campo == "duracion_horas" and not validar_entrada_duracion(valor):
            mostrar_mensaje(page, f"El campo '{campo}' tiene un formato de duración inválido. Debe ser un número entero mayor que 0.", "advertencia")
            return False
        if campo == "estado" and valor not in ["Alta", "Baja", "Pendiente"]:
            mostrar_mensaje(page, f"El campo '{campo}' tiene un valor inválido. Debe ser 'Alta', 'Baja' o 'Pendiente'.", "advertencia")
            return False
        if campo == "password" and len(valor) < 4:
            mostrar_mensaje(page, f"El campo '{campo}' tiene un formato de contraseña inválido. Debe tener al menos 4 caracteres.", "advertencia")
            return False
    return True