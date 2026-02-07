from datetime import datetime
import flet as ft
from database.crud import *
from utils.elements import *
from utils.validaciones import *
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
        '''Guarda en la base de datos un nuevo apunte
        para la colección de cursos y otro para la del docente implicado'''

        if not titulo.value.strip() or not descripcion.value.strip() or not precio.value or not duracion.value:
            mostrar_mensaje(page, "Alguno de los campos se encuentran vacíos. Por favor, rellénelos previamente antes de continuar.", "advertencia")
            return
        precio_valor = 0.0
        duracion_valor = 0

        try:
            precio_str = precio.value.replace(',', '.')
            precio_valor = float(precio_str)
            duracion_valor = int(duracion.value)

        except ValueError:
            mostrar_mensaje(page, "El precio o la duración deben ser números válidos.", "error")
            return
    
        try:
            id_curso_correlativo = obtener_ultimo_id_curso()
            if not page.login_data:
                 mostrar_mensaje(page, "Error de sesión: No hay usuario logueado.", "error")
                 return
                 
            info_docente = obtener_informacion_perfil_usuario_docente(page.login_data["user_email"])
            docente_id_seleccionado = info_docente['_id']
            
            datos_docente = obtener_docente_por_id(docente_id_seleccionado)
            nombre_docente = datos_docente['nombre'] + " " + datos_docente['apellidos']

            crear_curso(
                id = id_curso_correlativo,
                titulo=titulo.value,
                descripcion=descripcion.value,
                precio=precio_valor,      
                duracion=duracion_valor,   
                docente_id=docente_id_seleccionado,
                docente_nombre=nombre_docente
            )

            mostrar_mensaje(page, "Se ha añadido y asignado un nuevo curso correctamente.", "info")
            dlg.open = False
            page.update()


        except Exception as e:
            print(f"Error detallado: {e}") # Útil para depurar en consola
            mostrar_mensaje(page, "Ha ocurrido un error inesperado al guardar el curso.", "error")
            return

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
        if not titulo.value.strip() or not descripcion.value.strip() or not duracion.value or not precio.value:
            mostrar_mensaje(page, "Alguno de los campos se encuentran vacíos. Por favor, rellénelos previamente antes de continuar.", "advertencia")
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
