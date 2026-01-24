import flet as ft
from database.crud import *
from utils.elements import *


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def load_dashboard_view():
    matriculas = obtener_todas_las_matriculas()
    total_enrollments = len(matriculas)
    datos_cursos = obtener_datos_cursos()
    pending_count = sum(1 for e in matriculas if e['status'] == "pendiente")
    revenue = sum(next(c['precio'] for c in datos_cursos if c['_id'] == e['curso_id']) for e in matriculas if e['status'] == "pagado")

    content_area.content = ft.Column([
        ft.Text("Dashboard", size=30, weight="bold"),
        ft.Divider(),
        ft.Row([
            MetricCard("Total Matrículas", total_enrollments, ft.Icons.PEOPLE, ft.Colors.BLUE),
            MetricCard("Pendientes de Pago", pending_count, ft.Icons.PENDING_ACTIONS, ft.Colors.ORANGE),
            MetricCard("Ingresos Totales", f"${revenue:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.GREEN),
        ], wrap=True, spacing=20),
            ft.Container(height=30),
            ft.Text("Accesos rápidos", size=20),
            ft.Text("Aquí irían gráficos o últimas actividades...", color=ft.Colors.GREY_400)
    ], scroll="auto")
    content_area.update()