import flet as ft
from database.crud import *
from utils.elements import *


contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_dashboard_docente(current_user:dict):
    cursos_asociados = obtener_todos_los_cursos_docente(current_user['email'])
    cursos_id = [curso["curso_id"] for curso in cursos_asociados]
    total_enrollments = len(cursos_asociados)
    total_alumnos = obtener_alumnos_de_un_curso(cursos_id)
    total_alumnos = len(total_alumnos)

    contenedor.content = ft.Column([
        ft.Text("Dashboard", size=30, weight="bold"),
        ft.Divider(),
        ft.Row([
            tarjeta_metrica("Total de cursos impartidos", total_enrollments, ft.Icons.SCHOOL, ft.Colors.BLUE),
            tarjeta_metrica("Total de alumnos", total_alumnos, ft.Icons.PERSON, ft.Colors.PURPLE),
            # MetricCard("Pendientes de Pago", pending_count, ft.Icons.PENDING_ACTIONS, ft.Colors.ORANGE),
            # MetricCard("Ingresos Totales", f"${revenue:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.GREEN),
        ], wrap=True, spacing=20),
            ft.Container(height=30),
            ft.Text("Accesos rápidos", size=20),
            ft.Text("Aquí irían gráficos o últimas actividades...", color=ft.Colors.GREY_400)
    ], scroll="auto")
    contenedor.update()