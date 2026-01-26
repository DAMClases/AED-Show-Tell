import flet as ft
from datetime import datetime
from database.crud import *

# --- SIMULACIÓN DE BASE DE DATOS (Datos en memoria) ---
courses_data = [
    {"id": 1, "name": "Python desde Cero", "price": 99.99},
    {"id": 2, "name": "Desarrollo Web Fullstack", "price": 199.50},
    {"id": 3, "name": "Data Science con Pandas", "price": 150.00},
]

enrollments_data = [
    {"id": 101, "student": "Juan Pérez", "course_id": 1, "status": "Pagado", "date": "2023-10-25"},
    {"id": 102, "student": "María García", "course_id": 2, "status": "Pendiente", "date": "2023-10-26"},
    {"id": 103, "student": "Carlos López", "course_id": 1, "status": "Cancelado", "date": "2023-10-27"},
    {"id": 104, "student": "Ana Ruiz", "course_id": 3, "status": "Pendiente", "date": "2023-10-28"},
]

def get_course_name(course_id):
    for course in courses_data:
        if course['id'] == course_id:
            return course['name']
    return "Desconocido"

# --- Componentes de UI Reutilizables ---

def StatusBadge(status):
    """Crea una etiqueta de color según el estado"""
    colors = {
        "pagado": ft.Colors.GREEN_400,
        "pendiente": ft.Colors.ORANGE_400,
        "cancelado": ft.Colors.RED_400,
    }
    color = colors.get(status, ft.Colors.GREY_400)
    return ft.Container(
        content=ft.Text(status, color=ft.Colors.WHITE, size=12, weight="bold"),
        bgcolor=color,
        # Ajuste: Uso de clase Padding y BorderRadius para evitar advertencias
        padding=ft.Padding(10, 5, 10, 5),
        border_radius=ft.BorderRadius(15, 15, 15, 15),
        alignment=ft.Alignment(0, 0)
    )

def MetricCard(title, value, icon, color):
    """Tarjeta pequeña para el Dashboard"""
    return ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Row([
                ft.Icon(icon, color=color, size=40),
                ft.Column([
                    ft.Text(title, size=14, color=ft.Colors.GREY_500),
                    ft.Text(str(value), size=24, weight="bold")
                ], spacing=5)
            ], alignment="spaceBetween")
        )
    )

# --- APLICACIÓN PRINCIPAL ---

def main(page: ft.Page):
    page.title = "Panel Admin - Matrículas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    current_user = { ####
        "email": None,
        "role": None,
    }
    content_area = ft.Container(expand=True, padding=20)

    # --- Lógica de Actualización de Estados ---
    
    def change_enrollment_status(e, alumno_id, curso_id, new_status):

        actualizar_estado_curso(alumno_id, curso_id, new_status)
                
        load_matricula_view()
        page.update()

    def show_course_details(curso_id):
        curso = obtener_curso_por_id(curso_id)
        if not curso:
            print(f"Curso con ID {curso_id} no encontrado.")
            return

        dlg = ft.AlertDialog(
            title=ft.Text(f"Detalles del Curso: {curso['titulo']}"),
            content=ft.Column([
                ft.Text(f"ID: {curso['_id']}"),
                ft.Text(f"Descripción: {curso['descripcion']}"),
                ft.Text(f"Precio: ${curso['precio']:.2f}"),
                ft.Text(f"Duración: {curso['duracion_horas']} horas"),
                ft.Text(f"Instructor: {curso['instructor']['nombre']}"),
            ], spacing=10),
            actions=[
                ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
            ],
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def show_status_dialog(alumno_id, curso_id, current_status):
        print(f"Abriendo diálogo para Alumno: {alumno_id}, Curso: {curso_id}")

        def on_click_status(e, new_status):
            change_enrollment_status(e, alumno_id, curso_id, new_status)
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(f"Editar: {curso_id}"),
            content=ft.Text(f"Alumno: {alumno_id}"),
            actions=[
                ft.Button("PAGADO", on_click=lambda e: on_click_status(e, "pagado"), bgcolor="green", color="white"),
                ft.Button("PENDIENTE", on_click=lambda e: on_click_status(e, "pendiente"), bgcolor="orange", color="white"),
                ft.Button("CANCELADO", on_click=lambda e: on_click_status(e, "cancelado"), bgcolor="red", color="white"),
                ft.Button("CERRAR", on_click=lambda _: (setattr(dlg, "open", False), page.update()))
            ],
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- VISTAS (Páginas internas) ---

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

    def load_matricula_view():
        rows = []
        matriculas = obtener_todas_las_matriculas()
        
        for matricula in matriculas:
            id_alumno = matricula.get("alumno_id")
            cod_curso = matricula.get("curso_id")
            estado_actual = matricula.get("status")
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(matricula["curso_id"])),
                        ft.DataCell(ft.Text(matricula["estudiante"], weight="bold")),
                        ft.DataCell(ft.Text(matricula["curso_nombre"])),
                        ft.DataCell(StatusBadge(matricula["status"])),
                        ft.DataCell(ft.Text(matricula["fecha_matricula"])),
                        ft.DataCell(
                        ft.IconButton(
                            ft.Icons.EDIT,
                            # PASAMOS AMBOS IDs: Alumno y Curso
                            on_click=lambda e, a_id=id_alumno, c_id=cod_curso, s=estado_actual: 
                                show_status_dialog(a_id, c_id, s)
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

        content_area.content = ft.Column([
            ft.Row([
                ft.Text("Gestión de Matrículas", size=30, weight="bold"),
                ft.Button("Nueva Matrícula Manual", icon=ft.Icons.ADD,on_click=lambda e: show_add_enrollment_dialog()) 
            ], alignment="spaceBetween"),
            ft.Divider(),
            # Usamos una Column envuelta para permitir el scroll de la tabla
            ft.Column([table], scroll="auto", expand=True), 
        ], expand=True)
        content_area.update()

    # Cursos
    def load_cursos_view():
        
        datos_cursos = obtener_datos_cursos()
        course_cards = [CursoCard(curso) for curso in datos_cursos]
        content_area.content = ft.Column([
            ft.Row([
            ft.Text("Gestión de Cursos", size=30, weight="bold"),
            ft.Button("Agregar Nuevo Curso", icon=ft.Icons.ADD, on_click=lambda e: show_add_course_dialog())
            ], alignment="spaceBetween"),
            ft.Divider(),
            ft.Row(course_cards, wrap=True, spacing=20, run_spacing=20)
        ], scroll="auto")
        content_area.update()

    def load_usuario_view():    
        datos_usuario = obtener_informacion_perfil_usuario_admin(current_user["email"])
        contenido_mostrable = info_panel(datos_usuario)
        content_area.content = ft.Column([
            ft.Row([
            ft.Text("Información de la cuenta", size=30, weight="bold"),], alignment="spaceBetween"),
            ft.Divider(),
            ft.Row(contenido_mostrable, expand=True)], 
        scroll="auto")
        content_area.update()
    def CursoCard(curso):
        """Tarjeta para mostrar información del curso"""
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text(curso['titulo'], size=18, weight="bold"),
                    ft.Text(f"Precio: ${curso['precio']:.2f}", size=14, color=ft.Colors.GREY_600),
                    ft.Text(f"Duración: {curso['duracion_horas']} horas", size=14, color=ft.Colors.GREY_600),
                    ft.Text(f"Instructor: {curso['instructor']['nombre']}", size=14, color=ft.Colors.GREY_600),
                    ft.Button("Ver Detalles", bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE, on_click=lambda e, c_id=curso['_id']: show_course_details(c_id))
                ], spacing=10)
            )
        )
    def info_panel(usuario):
        '''Vista que he construido para generar los datos del usuario.'''
        return ft.Container(
            ft.Column([
                ft.Text(f"Nombre: {usuario['nombre']}", size=14, weight="bold"),
                ft.Text(f"Apellidos: {usuario['apellidos']}", size=14, weight="bold"),
                ft.Text(f"Nombre de usuario: {usuario['email']}", size=14, weight="bold"),
                ft.Divider(),
                ft.Text(f"Teléfono: {usuario['telefono']}", size=14, color=ft.Colors.GREY_600),
                ft.Text(f"Dirección: {usuario['direccion']}", size=14, color=ft.Colors.GREY_600),
                ft.Text(f"E-mail: {usuario['email']}", size=14, color=ft.Colors.GREY_600)], spacing=10))
    
    def show_add_course_dialog():

        titulo = ft.TextField(label="Título del curso")
        descripcion = ft.TextField(label="Descripción", multiline=True)
        precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
        duracion = ft.TextField(label="Duración (horas)", keyboard_type=ft.KeyboardType.NUMBER)
        
        docente_id_seleccionado = None

        def set_docente(docente_id):
            nonlocal docente_id_seleccionado
            docente_id_seleccionado = docente_id
        
        docente_id = AutocompletarCampo(set_docente, "Docente")

        def guardar_curso(e):
            crear_curso(
                titulo=titulo.value,
                descripcion=descripcion.value,
                precio=float(precio.value),
                duracion=int(duracion.value),
                docente_id=docente_id.value,
                docente_nombre=obtener_docente_por_id(docente_id.value)['nombre'] + " " + obtener_docente_por_id(docente_id.value)['apellidos']
            )
            dlg.open = False
            load_cursos_view()
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Agregar Nuevo Curso"),
            content=ft.Column([
                titulo,
                descripcion,
                precio,
                duracion,
                docente_id
            ], tight=True),
            actions=[
                ft.Button("Guardar", on_click=guardar_curso),
                ft.Button("Cancelar", on_click=lambda _: setattr(dlg, "open", False))
            ]
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # Autocompletar
    def AutocompletarCampo(on_select, campo:str):
        match campo:
            case "Curso":
                datos = obtener_datos_cursos()
            case "Docente":
                datos = obtener_docentes()
            case "Alumno":
                datos = obtener_todos_los_alumnos()


        input = ft.TextField(label=campo,
                             on_change=lambda e: on_change(e),
        )

        list_view = ft.ListView(
            height=220,
            spacing=5
        )

        dropdown = ft.Container(
            content=list_view,
            bgcolor=ft.Colors.SURFACE,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=6,
            padding=5,
            visible=False,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            ),
        )


        def on_change(e):
            texto = input.value.lower().strip()
            list_view.controls.clear()

            if not texto:
                dropdown.visible = False
                input.page.update()
                return

            
            for dato in datos:
                match campo:
                    case "Curso":
                        texto_busqueda = dato["titulo"]
                    case "Docente":
                        texto_busqueda = f"{dato['nombre']} {dato['apellidos']}"
                    case "Alumno":
                        texto_busqueda = f"{dato['nombre']} {dato['apellidos']}"
                if texto in texto_busqueda.lower():
                    list_view.controls.append(
                        ft.ListTile(
                            title=ft.Text(texto_busqueda),
                            on_click=lambda e, c=dato: select(c)
                        )
                    )

            dropdown.visible = len(list_view.controls) > 0
            input.page.update()

        def select(dato):
            input.value = dato["titulo"] if campo=="Curso" else f"{dato['nombre']} {dato['apellidos']}"
            input.data = dato["_id"]
            dropdown.visible = False
            input.page.update()
            on_select(dato["_id"])

        return ft.Column(
            [
                input,
                dropdown,
            ],
            spacing=2,
        )

    # Matrículas
    
    def show_add_enrollment_dialog():

        curso_id_seleccionado = None
        alumno_id_seleccionado = None

        def set_curso(cid):
            nonlocal curso_id_seleccionado
            curso_id_seleccionado = cid
        
        def set_alumno(alumno_id):
            nonlocal alumno_id_seleccionado
            alumno_id_seleccionado = alumno_id

        curso_autocomplete = AutocompletarCampo(set_curso, "Curso")
        alumno_autocomplete = AutocompletarCampo(set_alumno, "Alumno")

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
            crear_matricula(
                alumno_id=alumno_id_seleccionado,
                curso_id=curso_id_seleccionado,
                status=estado.value,
                fecha_matricula=datetime.now().strftime("%Y-%m-%d")
            )
            dlg.open = False
            load_matricula_view()
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Nueva Matrícula Manual"),
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
    # Ventanas de edición

    def editar_matricula(matricula_id):
        ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text(f"Editar Matrícula ID: {matricula_id}", size=18, weight="bold"),
                    # Aquí irían los campos de edición
                    ft.Text("Funcionalidad en desarrollo...", color=ft.Colors.GREY_600)
                ], spacing=10)
            )
        )


    # --- Layout Principal (Sidebar + Contenido) ---
    
    def build_admin_layout():
        def on_nav_change(e):
            idx = e.control.selected_index
            if idx == 0: load_dashboard_view()
            elif idx == 1: load_matricula_view()
            elif idx == 2:load_cursos_view()
            elif idx == 3:load_usuario_view()
            elif idx == 4:login_screen()


        sidebar = ft.NavigationRail(
            selected_index=0,
            label_type="all",
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
                ft.NavigationRailDestination(icon=ft.Icons.RECEIPT_LONG_OUTLINED, selected_icon=ft.Icons.RECEIPT_LONG, label="Matrículas"),
                ft.NavigationRailDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Cursos"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil de usuario"),
                ft.NavigationRailDestination(icon=ft.Icons.LOGOUT, label="Cerrar sesión")
            ],
            on_change=on_nav_change
        )

        layout = ft.Row([sidebar, ft.VerticalDivider(width=1), content_area], expand=True)
        page.add(layout)
        load_dashboard_view()

    def build_user_layout():
        def on_nav_change(e):
            idx = e.control.selected_index
            if idx == 0: load_dashboard_view()
            elif idx == 1:
                content_area.content = ft.Text("Vista de Cursos...")
                content_area.update()

        sidebar = ft.NavigationRail(
            selected_index=0,
            label_type="all",
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
                ft.NavigationRailDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Cursos"),
            ],
            on_change=on_nav_change
        )

        layout = ft.Row([sidebar, ft.VerticalDivider(width=1), content_area], expand=True)
        page.add(layout)
        load_dashboard_view()
    # --- Pantalla de Login ---
    
    def login_screen():
        page.overlay.clear()
        page.clean()

        user_input = ft.TextField(label="Usuario", width=300)
        pass_input = ft.TextField(label="Contraseña", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)

        def login_click(e):
            resultado_login = buscar_usuario_por_email(user_input.value, pass_input.value)
            current_user["email"] = "cristophermc@gmail.com"
            current_user["role"] = "admin"
            page.clean()
            build_admin_layout()
            return
            if resultado_login[0]:
                
                current_user["email"] = user_input.value
                current_user["role"] = resultado_login[1]
                page.clean()
                match resultado_login[1]:
                    case 'usuario':
                        build_user_layout()
                    case 'docente':
                        pass
                    case 'admin':
                        build_admin_layout()
            else:
                error_text.value = "Error: Usuario/Contraseña incorrectos."
                page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=60, color=ft.Colors.BLUE),
                    ft.Text("Acceso Administrativo", size=24, weight="bold"),
                    user_input,
                    pass_input,
                    error_text,
                    ft.Button("Entrar", on_click=login_click, width=300)
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        )

    login_screen()

# Ajuste: ft.run() es el estándar actual sobre ft.app()
if __name__ == "__main__":
    ft.run(main)