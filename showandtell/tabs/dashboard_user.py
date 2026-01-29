import flet as ft
from database.crud import *
from utils.elements import *


content_area: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global content_area, page
    content_area = container
    page = pg

def load_dashboard_user_view(current_user:dict):
    cursos_asociados = obtener_todos_los_cursos_de_un_alumno(current_user['email'])
    cursos_id = [curso["curso_id"] for curso in cursos_asociados]
    total_enrollments = len(cursos_asociados)
    total_alumnos = obtener_alumnos_de_un_curso(cursos_id)
    total_alumnos = len(total_alumnos)

    content_area.content = ft.Column([
        ft.Text("Dashboard", size=30, weight="bold"),
        ft.Divider(),
        ft.Row([
            MetricCard("Total de cursos", total_enrollments, ft.Icons.SCHOOL, ft.Colors.BLUE),
            MetricCard("Cursos disponibles en la plataforma", total_alumnos, ft.Icons.PERSON, ft.Colors.PURPLE),
            # MetricCard("Pendientes de Pago", pending_count, ft.Icons.PENDING_ACTIONS, ft.Colors.ORANGE),
            # MetricCard("Ingresos Totales", f"${revenue:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.GREEN),
        ], wrap=True, spacing=20),
            ft.Container(height=30),
            ft.Text("Accesos rápidos", size=20),
            ft.Text("Aquí irían gráficos o últimas actividades...", color=ft.Colors.GREY_400)
    ], scroll="auto")
    content_area.update()

# MetricCard("Total de cursos impartidos", None, ft.Icons.SCHOOL, ft.Colors.BLUE),
# MetricCard("Total de alumnos", None, ft.Icons.PERSON, ft.Colors.PURPLE),
# MetricCard("Pendientes de Pago", pending_count, ft.Icons.PENDING_ACTIONS, ft.Colors.ORANGE),
# MetricCard("Ingresos Totales", f"${revenue:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.GREEN),



##################################### VISTA DEL ALUMNO ###################################
#CURSOS DEL ALUMNO                                                                       #
##########################################################################################

# def load_dashboard_user_view(current_user:dict):
#     from utils.elements import CursoCard
    
#     # cursos_asociados = obtener_todos_los_cursos_docente(current_user['email'])
#     # cursos_id = [curso["curso_id"] for curso in cursos_asociados]
#     # total_enrollments = len(cursos_asociados)
#     # total_alumnos = obtener_alumnos_de_un_curso(cursos_id)
#     # total_alumnos = len(total_alumnos)
#     datos_cursos = obtener_datos_cursos()
#     course_cards = [CursoCard(page,curso) for curso in datos_cursos]
#     content_area.content = ft.Column([
#         ft.Row([
#         ft.Text("Dashboard", size=30, weight="bold")], alignment="spaceBetween"),
#         ft.Divider(),
#         ft.Row(course_cards, wrap=True, spacing=20, run_spacing=20)
#     ], scroll="auto")
#     content_area.update()