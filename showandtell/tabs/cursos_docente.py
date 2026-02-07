from datetime import datetime
import flet as ft
from database.crud import *
from utils.elements import *

contenedor: ft.Container
page: ft.Page

def setup(container: ft.Container, pg: ft.Page):
    global contenedor, page
    contenedor = container
    page = pg

def cargar_vista_cursos_disponibles(usuario_actual:dict):
    '''Carga la vista estilo tree de los datos de los cursos que tiene
    asociado un docente.'''

    rows = []
    cursos = obtener_todos_los_cursos_docente(usuario_actual['email'])
    cursos_id = [curso["curso_id"] for curso in cursos]
    recuento = obtener_todos_los_cursos_asociados_alumno(cursos_id)
    datos_curso = obtener_informacion_curso(cursos_id)
    indice = 0
    for _ in cursos:
        datos_fila_edit = [cursos[indice]['titulo'], datos_curso[indice]['descripcion'], datos_curso[indice]['duracion_horas'], datos_curso[indice]['precio'],cursos[indice]['curso_id']]
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(cursos_id[indice])),
                    ft.DataCell(ft.Text(cursos[indice]['titulo'], weight="bold")),
                    ft.DataCell(ft.Text((datos_curso[indice]['descripcion']), weight="bold")),
                    ft.DataCell(ft.Text((datos_curso[indice]['duracion_horas']), weight="bold")),
                    ft.DataCell(ft.Text(recuento[indice], weight="bold")),
                    ft.DataCell(ft.IconButton(ft.Icons.EDIT, on_click=lambda e, info=datos_fila_edit: mostrar_modificar_curso(info, usuario_actual)))
                ]
            )
        )
        indice +=1
        
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre del curso")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Horas")),
            ft.DataColumn(ft.Text("Alumnos")),
            ft.DataColumn(ft.Text("Editar curso")),

        ],
        rows=rows,
        border=ft.Border(ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200"), ft.BorderSide(1, "grey200")),
        heading_text_style=ft.TextStyle(weight="bold", color=ft.Colors.BLUE_GREY_900),
    )

    contenedor.content = ft.Column([
        ft.Row([
            ft.Text("Gestión de cursos", size=30, weight="bold"),
            ft.Button("Añadir un curso", icon=ft.Icons.ADD,on_click=lambda e: mostrar_popup_añadir_curso_docente()) 
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Column([table], scroll="auto", expand=True), 
    ], expand=True)
    contenedor.update()

#################################### Añadir un curso nuevo #################################

def mostrar_popup_añadir_curso_docente():
    '''La modificación de este submenú es que el docente estará bloqueado y cargado previamente.'''
    titulo = ft.TextField(label="Título del curso")
    descripcion = ft.TextField(label="Descripción del curso", multiline=True)
    precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
    duracion = ft.TextField(label="Duración", keyboard_type=ft.KeyboardType.NUMBER)
    
    


    def guardar_nuevo_curso():

        if not titulo.value:
            pass
        if not descripcion.value:
            pass
        if not precio.value:
            pass
        titulo = titulo.value
        descripcion = descripcion.value
        
        precio_str = precio.value.replace(',', '.')
        precio_valor = float(precio_str)
        id_curso_correlativo = obtener_ultimo_id_curso()
        docente_id_seleccionado = obtener_informacion_perfil_usuario_docente(page.login_data["user_email"])['_id']

        crear_curso(
            id = id_curso_correlativo,
            titulo=titulo.value,
            descripcion=descripcion.value,
            precio=precio_valor,
            duracion=int(duracion.value),
            docente_id=docente_id_seleccionado,
            docente_nombre=obtener_docente_por_id(docente_id_seleccionado)['nombre'] + " " + obtener_docente_por_id(docente_id_seleccionado)['apellidos']
        )
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
            title=ft.Text("Añadir nuevo curso"),
            content=ft.Column([
                titulo,
                descripcion,
                precio,
                duracion,
            ], tight=True),
            actions=[
                
                ft.Button("Guardar", on_click=guardar_nuevo_curso),
                ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
            ]
        )
    page.overlay.append(dlg)
    dlg.open = True
    page.update() 
def mostrar_modificar_curso(datos, usuario_actual):
    print(datos)
    titulo = ft.TextField(label="Título del curso", value=datos[0])
    descripcion = ft.TextField(label="Descripción", value=datos[1], multiline=True)
    duracion = ft.TextField(label="Duración (horas)", value=datos[2], keyboard_type=ft.KeyboardType.NUMBER)
    precio = ft.TextField(label="Precio", value=datos[3], keyboard_type=ft.KeyboardType.NUMBER)

    def modificar_curso(e):
        '''Acción cuando se clica modificar curso'''
        if not titulo.value:
            mostrar_mensaje(page, "El campo título se encuentra vacío.", "advertencia")
            return
        if not descripcion.value:
            mostrar_mensaje(page, "El campo descripción se encuentra vacío.", "advertencia")
            return
        if not duracion.value:
            mostrar_mensaje(page, "El campo duración se encuentra vacío.", "advertencia")
            return
        if not precio.value: 
            mostrar_mensaje(page, "El campo precio se encuentra vacío.", "advertencia")
            return

        duracion_val = 0
        precio_val = 0.0

        try:
            precio_val = (str(precio.value).replace(',', '.'))
            precio_val = float(precio_val)
            duracion_val = int(duracion.value)
        except ValueError:
            mostrar_mensaje(page, "El precio o la duración deben ser números válidos.", "error")
            return

        datos_crud = [titulo.value, descripcion.value, duracion_val, precio_val, datos[4]]
        
        if modificar_curso_vista_docente(datos_crud):
            mostrar_mensaje(page, "Se ha cambiado la información del curso.", "info")
            dlg.open = False
            page.update()
            cargar_vista_cursos_disponibles(usuario_actual)
        else:
            mostrar_mensaje(page, "Ha ocurrido un error inesperado durante el procesamiento de los datos.", "error")
            return

    dlg = ft.AlertDialog(
        title=ft.Text("Modificar curso"),
        content=ft.Column([
            titulo,
            descripcion,
            duracion,
            precio,
        ], tight=True),
        actions=[
            ft.Button("Guardar", on_click=modificar_curso),
            ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
        ]
    )
    
    page.overlay.append(dlg)
    dlg.open = True
    page.update()
