from datetime import datetime
import flet as ft
from database.crud import *
from utils.elements import *
from utils.validaciones import mostrar_mensaje

contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_vista_matriculas_admin():
    rows = []
    matriculas = obtener_todas_las_matriculas()
    
    for matricula in matriculas:
        id_alumno = matricula.get("alumno_id")
        cod_curso = matricula.get("curso_id")
        estado_actual = matricula.get("estado")
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(matricula["curso_id"])),
                    ft.DataCell(ft.Text(matricula["estudiante"], weight="bold")),
                    ft.DataCell(ft.Text(matricula["curso_nombre"])),
                    ft.DataCell(etiqueta_estado(matricula["estado"])),
                    ft.DataCell(ft.Text(matricula["fecha_matricula"])),
                    ft.DataCell(
                    ft.IconButton(
                        ft.Icons.EDIT,
                        # PASAMOS AMBOS IDs: Alumno y Curso
                        on_click=lambda e, a_id=id_alumno, c_id=cod_curso, s=estado_actual: 
                            mostrar_popup_estado_matricula(a_id, c_id, s)
                    )
                ),
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Estudiante")),
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=rows,
        border=ft.Border(ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200")),
        heading_text_style=ft.TextStyle(weight="bold", color=ft.Colors.BLUE_GREY_900),
    )

    contenedor.content = ft.Column([
        ft.Row([
            ft.Text("Gestión de Matrículas", size=30, weight="bold"),
            ft.Button("Nueva Matrícula", icon=ft.Icons.ADD,on_click=lambda e: mostrar_popup_añadir_matricula()) 
        ], alignment="spaceBetween"),
        ft.Divider(),
        # Usamos una Column envuelta para permitir el scroll de la tabla
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    contenedor.update()

def mostrar_popup_estado_matricula(alumno_id, curso_id, current_estado):
    print(f"Abriendo diálogo para Alumno: {alumno_id}, Curso: {curso_id}")

    def on_click_estado(e, new_estado):
        cambiar_estado_matricula(e, alumno_id, curso_id, new_estado)
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text(f"Editar: {curso_id}"),
        content=ft.Text(f"Alumno: {alumno_id}"),
        actions=[
            ft.Button("PAGADO", on_click=lambda e: on_click_estado(e, "pagado"), bgcolor="green", color="white"),
            ft.Button("PENDIENTE", on_click=lambda e: on_click_estado(e, "pendiente"), bgcolor="orange", color="white"),
            ft.Button("CANCELADO", on_click=lambda e: on_click_estado(e, "cancelado"), bgcolor="red", color="white"),
            ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
        ],
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def cambiar_estado_matricula(e, alumno_id, curso_id, new_estado):

    actualizar_estado_matricula(alumno_id, curso_id, new_estado)
            
    cargar_vista_matriculas_admin()
    page.update()

def mostrar_popup_añadir_matricula():

    curso_id_seleccionado = None
    alumno_id_seleccionado = None

    def set_curso(cid):
        nonlocal curso_id_seleccionado
        curso_id_seleccionado = cid
    
    def set_alumno(alumno_id):
        nonlocal alumno_id_seleccionado
        alumno_id_seleccionado = alumno_id

    curso_autocomplete = autocompletar_campo(set_curso, "Curso")
    alumno_autocomplete = autocompletar_campo(set_alumno, "Alumno")

    estado = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("pendiente"),
            ft.dropdown.Option("pagado"),
            ft.dropdown.Option("cancelado"),
        ],
        value="pendiente"
    )

    def guardar_matricula(e):
        try:
            crear_matricula(
                alumno_id=alumno_id_seleccionado,
                curso_id=curso_id_seleccionado,
                estado=estado.value,
                fecha_matricula=datetime.now().strftime("%Y-%m-%d")
            )
        except ValueError as e:
            mostrar_mensaje(page, f"Error al crear matrícula: {e}", "error")
            print(f"Error al crear matrícula: {e}")
        else:
            dlg.open = False
            cargar_vista_matriculas_admin()
            page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Nueva Matrícula"),
        content=ft.Column([
            alumno_autocomplete,
            curso_autocomplete,
            estado
        ], tight=True),
        actions=[
            ft.Button("Guardar", on_click=guardar_matricula),
            ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
        ]
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()