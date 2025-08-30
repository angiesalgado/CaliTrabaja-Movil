# app/views/Inicio.py
import flet as ft
import asyncio
from flet import Icons
from app.components.nav import nav_bar
from app.components.menu_inferior import menu_inferior
from app.components.ModalReporte import ModalReporte
from app.components.ModalTarjetaCompleta import ModalTarjetaCompleta
from app.components.MenuTarjetasOpciones import menu_opciones


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

    # ---------------- INSTANCIA DE MODAL REPORTE Y TARJETA ----------------
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

    # ---------------- NAV SUPERIOR ----------------
    nav = nav_bar(
        page,
        page.width,
        show_back=False,  # 👉 en Inicio NO aparece la flecha
        show_explora=False,  # 👉 en Inicio NO aparece "Explora en"
        show_login_icon=True,
        on_login_click=lambda e: cambiar_pantalla("login")  # 👈 acción del botón
    )

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
        padding=14
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
            page.update()
            index = (index + 1) % len(frases)

    page.run_task(cambiar_frase)

    # ---------------- CATEGORÍAS ----------------

    categorias_titulo = ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    "Categorías",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_COLOR
                ),

                # "Ver todos" como texto clickeable en color negro
                ft.GestureDetector(
                    on_tap=lambda e: cambiar_pantalla("categorias"),
                    content=ft.Container(
                        padding=ft.padding.symmetric(horizontal=6, vertical=4),
                        content=ft.Text(
                            "Ver todos",
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color="black"  # <- forzamos negro aquí
                        )
                    )
                )
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
                    ),
                    on_click=lambda e: cambiar_pantalla("registro", origen="inicio")
                ),

                ft.TextButton(
                    text="Ingresar a mi cuenta",
                    style=ft.ButtonStyle(
                        color=TEXT_COLOR,
                        overlay_color=ft.Colors.GREY_200,
                        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
                    ),
                    on_click=lambda e: cambiar_pantalla("login")
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

    # ---------------- LAYOUT PRINCIPAL ----------------
    layout = ft.Column(
        controls=[
            nav,  # 🔹 Header / Navbar superior

            ft.Container(
                content=ft.Column(
                    controls=[
                        contenedor_frase,
                        categorias_titulo,
                        categorias_container,
                        publicaciones_container,
                        crear_cuenta_container,
                        destacados_container,
                    ],
                    spacing=10  # 👈 Separación entre secciones
                ),
                padding=ft.padding.only(top=15)  # 👈 Espacio entre nav y contenido
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE  # 👈 Permite scroll del contenido
    )

    # Agregar layout a la página
    page.add(layout)

    # ---------------- NAV INFERIOR (BottomAppBar) ----------------
    page.bottom_appbar = ft.BottomAppBar(
        content=menu,  # 🔹 Menú inferior (para navegación en móvil)
        bgcolor=ft.Colors.WHITE,
        elevation=0
    )

    # ---------------- RESPONSIVE ----------------
    def on_resize(e):
        # 🔹 Ajusta el navbar superior al cambiar el tamaño de la pantalla
        layout.controls[0] = nav_bar(page.width, ft.Ref[ft.Container]())
        page.update()

    page.on_resize = on_resize
    page.update()


