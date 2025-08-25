# app/views/Inicio.py
import flet as ft
import asyncio
from flet import Icons
from app.components.nav2 import nav2_bar
from app.components.menu_inferior import menu_inferior
from app.components.ModalReporte import ModalReporte


def pantalla_inicio(page: ft.Page, cambiar_pantalla):
    # ---------------- CONFIGURACIÓN GENERAL ----------------
    page.controls.clear()
    page.bottom_appbar = None
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.margin = 0
    page.spacing = 0
    page.window_maximized = True

    # Fuentes y tema
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.theme_mode = "light"
    page.title = "Inicio"

    PRIMARY_COLOR = "#3EAEB1"
    TEXT_COLOR = "#000000"
    BORDER_COLOR = "#D9D9D9"

    # ---------------- INSTANCIA DEL MODAL REPORTE ----------------
    modal_reporte = ModalReporte()
    page.overlay.append(modal_reporte.dialog)

    # ---------------- NAV SUPERIOR ----------------
    nav = nav2_bar(page.width, ft.Ref[ft.Container]())

    # ---------------- FRASES CAMBIANTES + BOTÓN INICIO SESIÓN ----------------
    frases = [
        ("Nosotros conectamos,", "tú decides."),
        ("Conecta, trabaja,", "crece"),
        ("Conectando habilidades para un futuro", "mejor.")
    ]

    frase_texto = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text(frases[0][0], size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    ft.Text(frases[0][1], size=17, color=PRIMARY_COLOR)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    contenedor_frase = ft.Container(
        content=frase_texto,
        alignment=ft.alignment.center,
        width=page.width,
        height=90,
        bgcolor="#D9D9D9",
        border_radius=ft.border_radius.all(2),
        margin=ft.margin.symmetric(horizontal=10, vertical=5),
        padding=10
    )

    boton_inicio_sesion = ft.Container(
        content=ft.ElevatedButton(
            text="Iniciar sesión",
            bgcolor=PRIMARY_COLOR,
            color=ft.Colors.WHITE,
            height=30,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=15)
            )
        ),
        alignment=ft.alignment.top_right,
        padding=ft.padding.only(right=15, top=6)
    )

    stack_header = ft.Stack(
        controls=[contenedor_frase, boton_inicio_sesion],
        width=page.width,
        height=95
    )

    async def cambiar_frase():
        index = 1
        while True:
            await asyncio.sleep(4)
            frase_texto.controls.clear()
            if index % len(frases) == 2:
                frase_texto.controls.append(
                    ft.Row(
                        controls=[ft.Text(frases[index][0], size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
                frase_texto.controls.append(
                    ft.Row(
                        controls=[ft.Text(frases[index][1], size=17, color=PRIMARY_COLOR)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            else:
                frase_texto.controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(frases[index][0], size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                            ft.Text(frases[index][1], size=17, color=PRIMARY_COLOR)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4
                    )
                )
            frase_texto.update()
            index = (index + 1) % len(frases)

    page.run_task(cambiar_frase)

    # ---------------- CATEGORÍAS ----------------
    categorias_titulo = ft.Container(
        content=ft.Row(
            [
                ft.Text("Categorías", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                ft.Text("Ver todos", size=14, weight=ft.FontWeight.W_600, color=TEXT_COLOR),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.symmetric(horizontal=15, vertical=8)
    )

    categorias = [
        {"nombre": "Categoría 1", "icono": "tecnico.svg"},
        {"nombre": "Categoría 2", "icono": "cuidado.svg"},
        {"nombre": "Categoría 3", "icono": "mascoteros.svg"},
        {"nombre": "Categoría 4", "icono": "educativos.svg"},
        {"nombre": "Categoría 5", "icono": "limpieza.svg"},
        {"nombre": "Categoría 6", "icono": "construccion.png"},
        {"nombre": "Categoría 7", "icono": "artisticos.svg"},
        {"nombre": "Categoría 8", "icono": "transporte.svg"},
        {"nombre": "Categoría 9", "icono": "culinarios.svg"},
        {"nombre": "Categoría 10", "icono": "salud_bien.svg"},
        {"nombre": "Categoría 11", "icono": "eventos.svg"}
    ]

    cat_items = [
        ft.Column(
            [
                ft.Container(content=ft.Image(src=cat["icono"], width=40, height=40),
                             width=55, height=55, bgcolor=ft.Colors.WHITE,
                             border=ft.border.all(1), border_radius=ft.border_radius.all(8),
                             alignment=ft.alignment.center),
                ft.Text(cat["nombre"], size=12, text_align=ft.TextAlign.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        for cat in categorias
    ]

    categorias_scroll = ft.Row(
        controls=cat_items,
        scroll=ft.ScrollMode.HIDDEN,
        spacing=12,
        expand=False,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    categorias_container = ft.Container(
        content=categorias_scroll,
        padding=ft.padding.symmetric(horizontal=15),
        height=105
    )

    # ---------------- FUNCIÓN TARJETA (ESTILO VERTICAL) ----------------
    def tarjeta_horizontal(nombre, profesion, descripcion, costo, calificacion=4):
        mostrar_boton = len(descripcion) > 70
        stars = ft.Row(
            [
                ft.Icon(ft.Icons.STAR if i < calificacion else ft.Icons.STAR_BORDER,
                        color=PRIMARY_COLOR, size=14)
                for i in range(5)
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
        )

        menu = ft.Container(
            content=ft.PopupMenuButton(
                icon=ft.Icons.MORE_HORIZ,
                icon_color=TEXT_COLOR,
                items=[
                    ft.PopupMenuItem(
                        content=ft.Row([ft.Icon(ft.Icons.BOOKMARK_BORDER, size=14, color=TEXT_COLOR),
                                        ft.Text("Guardar", color=TEXT_COLOR)], spacing=6)
                    ),
                    ft.PopupMenuItem(
                        content=ft.Row([ft.Icon(Icons.ERROR_OUTLINE, size=16, color=TEXT_COLOR),
                                        ft.Text("Reportar", color=TEXT_COLOR)], spacing=8),
                        on_click=lambda e: modal_reporte.show(page),
                    ),
                ]
            ),
            alignment=ft.alignment.top_right,
            padding=0,
            margin=ft.Margin(0, -10, -10, 0)
        )

        def mostrar_detalle(e):
            page.dialog = ft.AlertDialog(
                title=ft.Text("Descripción completa", weight=ft.FontWeight.BOLD),
                content=ft.Text(descripcion),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: setattr(page.dialog, "open", False))]
            )
            page.dialog.open = True
            page.update()

        return ft.Container(
            width=180,
            height=250,
            padding=8,
            bgcolor="white",
            border_radius=14,
            border=ft.border.all(1, BORDER_COLOR),
            content=ft.Stack(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(top=10),
                        content=ft.Column(
                            [
                                ft.CircleAvatar(radius=30, bgcolor=ft.Colors.GREY_300),
                                ft.Text(f"COP {costo}/h", size=11, color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text(nombre, weight=ft.FontWeight.BOLD, size=17, color=TEXT_COLOR,
                                        text_align=ft.TextAlign.CENTER),
                                stars,
                                ft.Text(profesion, size=14, weight=ft.FontWeight.W_500, color=TEXT_COLOR,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Text("Descripción:", size=12, color=ft.Colors.BLACK54,
                                        text_align=ft.TextAlign.CENTER),
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
                                ft.TextButton(
                                    "Ver más" if mostrar_boton else " ",
                                    on_click=mostrar_detalle if mostrar_boton else None,
                                    style=ft.ButtonStyle(
                                        color=PRIMARY_COLOR if mostrar_boton else "transparent",
                                        padding=0,
                                        text_style=ft.TextStyle(size=11)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    ),
                    menu
                ]
            )
        )

    # ---------------- PUBLICACIONES ----------------
    publicaciones = [
        {"nombre": "Claudia Henao", "profesion": "Fotógrafa", "descripcion": "Creatividad, técnica y detalle.", "costo": "30.000", "calificacion": 4},
        {"nombre": "Carlos Restrepo", "profesion": "Electricista", "descripcion": "Instalaciones eléctricas seguras para hogares y empresas. Soluciones rápidas y garantizadas.", "costo": "55.000", "calificacion": 5},
        {"nombre": "Roberto Gómez", "profesion": "Plomero", "descripcion": "Fugas, instalaciones y mantenimiento con servicio confiable.", "costo": "50.000", "calificacion": 3},
    ]

    publicaciones_container = ft.Column(
        [
            ft.Container(content=ft.Text("Te podría interesar", size=22, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                         alignment=ft.alignment.center, padding=ft.padding.only(bottom=5, top=15)),
            ft.Container(content=ft.Row(controls=[tarjeta_horizontal(**p) for p in publicaciones],
                                        spacing=15, scroll=ft.ScrollMode.HIDDEN),
                         padding=ft.padding.symmetric(horizontal=15))
        ]
    )

    # ---------------- SECCIÓN CREA UNA CUENTA ----------------
    crear_cuenta_container = ft.Container(
        bgcolor="#F8F8F8",
        border_radius=10,
        padding=20,
        margin=ft.margin.symmetric(horizontal=15, vertical=20),
        content=ft.Column(
            [
                ft.Text(
                    "¡Crea una cuenta y mejora tu experiencia!",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=TEXT_COLOR
                ),
                ft.ElevatedButton(
                    text="Crear cuenta",
                    bgcolor=PRIMARY_COLOR,
                    color="white",
                    height=32,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        padding=ft.padding.symmetric(horizontal=25),
                        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    )
                ),
                ft.TextButton(
                    text="Ingresar a mi cuenta",
                    style=ft.ButtonStyle(
                        color=TEXT_COLOR,
                        overlay_color=ft.Colors.GREY_200,
                        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    ),
                ),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ---------------- SECCIÓN SERVICIOS DESTACADOS ----------------
    destacados = [
        {"nombre": "Claudia Henao", "profesion": "Fotógrafa", "descripcion": "Con una combinación de técnica, creatividad y un profundo respeto por el instante.", "costo": "30.000", "calificacion": 5},
        {"nombre": "Carlos Restrepo", "profesion": "Diseñador Gráfico", "descripcion": "Transformo ideas en piezas visuales que comunican y conectan.", "costo": "40.000", "calificacion": 4},
        {"nombre": "Andrea López", "profesion": "Maestra de Inglés", "descripcion": "Clases personalizadas con enfoque comunicativo y dinámico.", "costo": "35.000", "calificacion": 5},
    ]

    otros_destacados = [
        {"nombre": "Roberto Gómez", "profesion": "Plomero", "descripcion": "Fugas, instalaciones y mantenimiento con servicio confiable.", "costo": "50.000", "calificacion": 4},
        {"nombre": "María Torres", "profesion": "Chef Personal", "descripcion": "Cocina gourmet en la comodidad de tu hogar.", "costo": "80.000", "calificacion": 5},
        {"nombre": "Juan Pérez", "profesion": "Entrenador Personal", "descripcion": "Rutinas adaptadas a tus objetivos y condición física.", "costo": "60.000", "calificacion": 5},
    ]

    destacados_container = ft.Column(
        [
            ft.Container(content=ft.Text("Servicios destacados", size=22, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                         alignment=ft.alignment.center, padding=ft.padding.only(bottom=5, top=15)),
            ft.Container(content=ft.Column(controls=[
                ft.Row(controls=[tarjeta_horizontal(**p) for p in destacados], spacing=15, scroll=ft.ScrollMode.HIDDEN),
                ft.Row(controls=[tarjeta_horizontal(**p) for p in otros_destacados], spacing=15, scroll=ft.ScrollMode.HIDDEN)
            ], spacing=20), padding=ft.padding.symmetric(horizontal=15))
        ]
    )

    # ---------------- MENÚ INFERIOR ----------------
    selected_index = 0

    def on_bottom_nav_click(index):
        nonlocal selected_index
        selected_index = index
        if index == 0:
            cambiar_pantalla("inicio")
        elif index == 2:
            cambiar_pantalla("categorias")
        elif index == 3:
            cambiar_pantalla("guardados")
        elif index == 4:
            cambiar_pantalla("menu")

    menu = menu_inferior(selected_index, on_bottom_nav_click)

    # ---------------- LAYOUT PRINCIPAL ----------------
    layout = ft.Column(
        controls=[
            nav,
            stack_header,
            categorias_titulo,
            categorias_container,
            publicaciones_container,
            crear_cuenta_container,
            destacados_container
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE
    )

    page.add(layout)

    page.bottom_appbar = ft.BottomAppBar(
        content=menu,
        bgcolor=ft.Colors.WHITE,
        elevation=0
    )

    # ---------------- RESPONSIVE ----------------
    def on_resize(e):
        layout.controls[0] = nav2_bar(page.width, ft.Ref[ft.Container]())
        page.update()

    page.on_resize = on_resize
    page.update()
