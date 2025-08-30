import flet as ft
from flet import Icons
from app.components.ModalReporte import ModalReporte
from app.components.nav import nav_bar
from app.components.menu_inferior import menu_inferior
from app.components.ModalTarjetaCompleta import ModalTarjetaCompleta
from app.components.MenuTarjetasOpciones import menu_opciones

def custom_expansion(page, title, controls_list):
    toggle_icon = ft.Icon(name=ft.Icons.KEYBOARD_ARROW_DOWN, color="#3EAEB1")


    styled_controls = []
    for control in controls_list:
        if isinstance(control, ft.Radio):
            control.label_style = ft.TextStyle(
                color="#666666",
                weight=ft.FontWeight.W_500
            )
        elif isinstance(control, ft.Checkbox):
            control.label_style = ft.TextStyle(
                color="#666666",
                weight=ft.FontWeight.W_500
            )
        styled_controls.append(control)

    content_column = ft.Column(styled_controls, visible=False, spacing=5)

    def toggle_visibility(e):
        content_column.visible = not content_column.visible
        toggle_icon.name = (
            ft.Icons.KEYBOARD_ARROW_UP if content_column.visible else ft.Icons.KEYBOARD_ARROW_DOWN
        )
        page.update()

    return ft.Column(
        [
            ft.GestureDetector(
                on_tap=toggle_visibility,
                content=ft.Row(
                    [
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color="black"
                        ),
                        toggle_icon,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
            content_column
        ],
        spacing=8
    )



def publicaciones(page: ft.Page, cambiar_pantalla, origen=None):
    # ---------------- CONFIGURACIÓN GENERAL ----------------
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.theme_mode = "light"
    page.bgcolor = "#F8F8F8"
    page.title = "Inicio"
    page.scroll = ft.ScrollMode.HIDDEN
    page.padding = 1

    PRIMARY_COLOR = "#3EAEB1"
    TEXT_COLOR = "#000000"
    BORDER_COLOR = "#D9D9D9"

    # ---------------- INSTANCIA DEL MODAL ----------------
    modal_reporte = ModalReporte()
    page.overlay.append(modal_reporte.dialog)

    modal_detalle = ModalTarjetaCompleta()
    page.overlay.append(modal_detalle.dialog)

    def abrir_modal_detalle(nombre, profesion, descripcion, costo, calificacion):
        print("CLICK -> abrir_modal_detalle:", nombre)  # <-- mira la consola donde corres Flet
        modal_detalle.set_content(nombre, profesion, descripcion, costo, calificacion)
        page.dialog = modal_detalle.dialog
        modal_detalle.dialog.open = True
        page.update()

    # 🔹 Overlay oscuro (para cerrar al hacer clic afuera)
    overlay = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        width=page.width,
        height=page.height,
        visible=False,
        on_click=lambda e: cerrar_filtros(),
    )

    # ---------------- PANEL FILTROS (oculto al inicio) ----------------
    filtros_panel = ft.Container(
        bgcolor="white",
        width=250,
        height=page.height,
        right=page.width,
        top=0,
        padding=0,
        animate_position=300,
        content=ft.Column(
            [

                ft.Container(
                    bgcolor="#F8F8F8",
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    content=ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                on_click=lambda e: cerrar_filtros(),
                                icon_color="#3EAEB1",  # Color de la flecha
                            ),
                            ft.Text(
                                "Filtrar",
                                size=20,
                                weight=ft.FontWeight.W_500, # Medium
                                font_family="Oswald",  # Fuente Oswald
                                color="black"
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ),


                ft.Container(
                    expand=True,
                    padding=ft.padding.all(15),
                    content=ft.Column(
                        [
                            custom_expansion(
                                page,
                                "Categorías",
                                [
                                    ft.Radio(value="todas", label="Todas"),
                                    ft.Radio(value="cat1", label="Categoría 1"),
                                    ft.Radio(value="cat2", label="Categoría 2"),
                                ]
                            ),

                            custom_expansion(
                                page,
                                "Subcategorías",
                                [
                                    ft.Checkbox(label="SubCategoría 1"),
                                    ft.Checkbox(label="SubCategoría 2"),
                                ]
                            ),

                            ft.Text(
                                "Fecha de publicación",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color="black"
                            ),
                            ft.Column(
                                [
                                    ft.Radio(
                                        value="todos",
                                        label="Todos",
                                        label_style=ft.TextStyle(
                                            color="#666666",
                                            weight=ft.FontWeight.W_500
                                        )
                                    ),
                                    ft.Radio(
                                        value="24h",
                                        label="Últimas 24 horas",
                                        label_style=ft.TextStyle(
                                            color="#666666",
                                            weight=ft.FontWeight.W_500
                                        )
                                    ),
                                    ft.Radio(
                                        value="semana",
                                        label="Esta semana",
                                        label_style=ft.TextStyle(
                                            color="#666666",
                                            weight=ft.FontWeight.W_500
                                        )
                                    ),
                                    ft.Radio(
                                        value="mes",
                                        label="Este mes",
                                        label_style=ft.TextStyle(
                                            color="#666666",
                                            weight=ft.FontWeight.W_500
                                        )
                                    ),
                                ],
                                spacing=5
                            )

                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO
                    )
                ),

                ft.Container(
                    content=ft.Row(
                        [
                            ft.ElevatedButton(
                                "Aplicar",
                                width=100,
                                height=40,
                                bgcolor=PRIMARY_COLOR,
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=30),
                                    padding=8
                                ),
                                on_click=lambda e: cerrar_filtros()
                            ),
                            ft.OutlinedButton(
                                "Limpiar filtros",
                                width=100,
                                height=40,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=30),
                                    padding=8,
                                    color="black"
                                ),
                                on_click=lambda e: print("Filtros limpiados")
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=ft.padding.only(bottom=10)
                )

            ],
            spacing=12,
        )
    )

    # ---------------- FUNCIONES PANEL ----------------
    def abrir_filtros(e=None):
        filtros_panel.right = page.width - 250
        overlay.visible = True
        page.update()

    def cerrar_filtros(e=None):
        filtros_panel.right = page.width  # vuelve a salir
        overlay.visible = False
        page.update()
    # ---------------- ENCABEZADO RESULTADOS ----------------
    header_resultados = ft.Container(
        content=ft.Column(
            [
                ft.ElevatedButton(
                    "Filtros",
                    bgcolor=PRIMARY_COLOR,
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=6)
                    ),
                    on_click=abrir_filtros
                ),
                ft.Text(
                    "124 resultados",
                    weight=ft.FontWeight.BOLD,
                    size=14,
                    color="#666666"
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=10,
        alignment=ft.alignment.top_left
    )

    # ---------------- PAGINACIÓN ----------------
    paginacion = ft.Container(
        content=ft.Row(
            [
                # Flecha izquierda en negro
                ft.IconButton(ft.Icons.CHEVRON_LEFT, tooltip="Anterior", icon_color=TEXT_COLOR),

                # Página activa
                ft.Container(
                    ft.Text("1", color="white"),  # círculo activo en blanco
                    bgcolor=PRIMARY_COLOR,
                    padding=6,
                    border_radius=12,
                ),
                # Páginas inactivas en negro
                ft.Container(ft.Text("2", color=TEXT_COLOR), padding=6, border_radius=12),
                ft.Container(ft.Text("3", color=TEXT_COLOR), padding=6, border_radius=12),
                ft.Container(ft.Text("4", color=TEXT_COLOR), padding=6, border_radius=12),
                ft.Container(ft.Text("...", color=TEXT_COLOR), padding=6, border_radius=12),

                # Flecha derecha en negro
                ft.IconButton(ft.Icons.CHEVRON_RIGHT, tooltip="Siguiente", icon_color=TEXT_COLOR),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        width=float("inf"),
        bgcolor="white",
        border_radius=12,
        padding=10,
        margin=ft.margin.all(8)
    )

    # ---------------- FUNCIÓN TARJETAS ----------------
    def tarjeta_horizontal(nombre, profesion, descripcion, costo, calificacion=4):
        mostrar_boton = len(descripcion) > 70

        stars = ft.Row(
            [ft.Icon(ft.Icons.STAR if i < calificacion else ft.Icons.STAR_BORDER,
                     color=PRIMARY_COLOR, size=14) for i in range(5)],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Menú con Guardar + Reportar
        menu = menu_opciones(page, modal_reporte, text_color=TEXT_COLOR, incluir_guardar=True)

        # Contenido principal
        tarjeta_contenido = ft.Container(
            padding=ft.padding.only(top=10),
            content=ft.Column(
                [
                    ft.CircleAvatar(radius=30, bgcolor=ft.Colors.GREY_300),
                    ft.Text(f"COP {costo}/h", size=11, color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Text(nombre, weight=ft.FontWeight.BOLD, size=17, color=TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER),
                    stars,
                    ft.Text(profesion, size=14, weight=ft.FontWeight.W_500, color=TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Descripción:", size=12, color=ft.Colors.BLACK54, text_align=ft.TextAlign.CENTER),

                    ft.Container(
                        content=ft.Text(
                            descripcion,
                            size=11,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color=TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER
                        ),
                        height=32,
                        alignment=ft.alignment.center
                    ),

                    # Botón Ver más con cursor y on_click
                    ft.Container(
                        content=ft.TextButton(
                            "Ver más" if mostrar_boton else "",
                            on_click=(lambda e: abrir_modal_detalle(nombre, profesion, descripcion, costo,
                                                                    calificacion)) if mostrar_boton else None,
                            style=ft.ButtonStyle(
                                color=PRIMARY_COLOR if mostrar_boton else "transparent",
                                padding=0,
                                text_style=ft.TextStyle(size=11)
                            )
                        ),
                        margin=ft.margin.only(top=-3)  # 🔹 lo sube 6px
                    )

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3
            )
        )

        return ft.Container(
            width=180,
            height=270,
            padding=8,
            bgcolor="white",
            border_radius=14,
            border=ft.border.all(1, BORDER_COLOR),
            content=ft.Stack(
                controls=[
                    tarjeta_contenido,
                    ft.Container(  # 👈 ahora sí lo posicionamos aquí
                        content=menu,
                        top=5,
                        right=5,
                    ),
                ]
            )
        )

    # ---------------- PUBLICACIONES ----------------
    publicaciones = [
        {"nombre": "Claudia Henao", "profesion": "Fotógrafa", "descripcion": "Creatividad, técnica y detalle y muchas cosas mas que quiero poner aqui .", "costo": "30.000", "calificacion": 4},
        {"nombre": "Carlos Restrepo", "profesion": "Electricista", "descripcion": "Instalaciones seguras y rápidas.", "costo": "55.000", "calificacion": 5},
        {"nombre": "Roberto Gómez", "profesion": "Plomero", "descripcion": "Reparaciones de fugas y mantenimiento.", "costo": "50.000", "calificacion": 3},
        {"nombre": "Andrea López", "profesion": "Diseñadora", "descripcion": "Diseños creativos e innovadores.", "costo": "40.000", "calificacion": 4},
        {"nombre": "María Torres", "profesion": "Chef Personal", "descripcion": "Cocina gourmet en tu casa.", "costo": "80.000", "calificacion": 5},
        {"nombre": "Juan Pérez", "profesion": "Entrenador Personal", "descripcion": "Rutinas adaptadas a tus objetivos.", "costo": "60.000", "calificacion": 5},
    ]

    # ---------------- GRID 2x2 ----------------
    filas = []
    for i in range(0, len(publicaciones), 2):
        fila = ft.Container(
            content=ft.Row(
                controls=[tarjeta_horizontal(**publicaciones[i])] +
                         ([tarjeta_horizontal(**publicaciones[i + 1])] if i + 1 < len(publicaciones) else []),
                spacing=7,
                alignment=ft.MainAxisAlignment.START  #  evita que se estiren de borde a borde
            ),
            padding=ft.padding.symmetric(horizontal=5)  #  mismo margen lateral que arriba
        )
        filas.append(fila)


    # Aquí organizamos a que interfaz devuelve dependiendo de dónde vino
    back_action = lambda e: cambiar_pantalla("categorias") if origen == "categorias" else cambiar_pantalla("menu")

    # ---------------- NAV SUPERIOR + CONTENIDO ----------------
    layout = ft.Column(
        [
            nav_bar(
                page,
                page.width,
                show_back=True,
                show_explora=True,
                on_back_click=back_action
            ),
            ft.Stack(
                [
                    ft.Column(
                        [
                            header_resultados,
                            ft.Column([paginacion], alignment=ft.MainAxisAlignment.CENTER, spacing=1),
                            ft.Column(filas, spacing=7, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    overlay,
                    filtros_panel
                ]
            )
        ],
        spacing=10,
        expand=True
    )

    # ---------------- MENÚ INFERIOR ----------------
    selected_index = 4

    def on_bottom_nav_click(index):
        if index == 0:  # Inicio
            cambiar_pantalla("inicio")
        elif index == 1:  # Categorias
            cambiar_pantalla("categorias")
        elif index == 2:  # Mensajes
            cambiar_pantalla("mensajes")
        elif index == 3:  # Guardados
            cambiar_pantalla("guardados")
        elif index == 4:  # Menú
            cambiar_pantalla("menu")

    menu = menu_inferior(selected_index, on_bottom_nav_click)

    page.bottom_appbar = ft.BottomAppBar(
        content=menu,
        bgcolor=ft.Colors.WHITE,
        elevation=0,
    )

    page.add(layout)
    page.update()




