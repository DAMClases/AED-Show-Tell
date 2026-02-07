import flet as ft
from database.crud import *
from utils.elements import *


contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_dashboard_admin():
    matriculas = obtener_todas_las_matriculas()
    total_enrollments = len(matriculas)
    datos_cursos = obtener_datos_cursos()
    pending_count = sum(1 for e in matriculas if e['estado'] == "pendiente")
    revenue = sum(next(c['precio'] for c in datos_cursos if c['_id'] == e['curso_id']) for e in matriculas if e['estado'] == "pagado")

    contenedor.content = ft.Column([
        ft.Text("Dashboard", size=30, weight="bold"),
        ft.Divider(),
        ft.Row([
            tarjeta_metrica("Total Matrículas", total_enrollments, ft.Icons.PEOPLE, ft.Colors.BLUE),
            tarjeta_metrica("Pendientes de Pago", pending_count, ft.Icons.PENDING_ACTIONS, ft.Colors.ORANGE),
            tarjeta_metrica("Ingresos Totales", f"${revenue:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.GREEN),
        ], wrap=True, spacing=20)
    ], scroll="auto")
    contenedor.update()