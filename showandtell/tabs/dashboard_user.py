import flet as ft
from database.crud import *
from utils.elements import *


contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_dashboard_alumno(current_user:dict):
    '''Carga los KPIs del usuario.'''
    cursos_asociados = obtener_cursos_de_alumno(current_user['email'])
    cursos_disponibles = obtener_cursos_disponibles_plataforma(cursos_asociados)
    contenedor.content = ft.Column([
        ft.Text("Dashboard", size=30, weight="bold"),
        ft.Divider(),
        ft.Row([
            tarjeta_metrica("Total de cursos", len(cursos_asociados['cursos']), ft.Icons.SCHOOL, ft.Colors.BLUE),
            tarjeta_metrica("Cursos disponibles en la plataforma", len(cursos_disponibles), ft.Icons.SCHOOL_SHARP, ft.Colors.GREEN),
        ], wrap=True, spacing=20),
            ft.Container(height=30),
    ], scroll="auto")
    contenedor.update()

