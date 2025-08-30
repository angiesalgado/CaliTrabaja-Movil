import flet as ft
from app.components.menu_inferior import menu_inferior
from app.components.ModalReporte import ModalReporte
from app.components.MenuTarjetasOpciones import menu_opciones


# ---------- NAV SUPERIOR ----------
def nav_superior(page_width: float, titulo="Título", on_back_click=lambda e: None):
    text_size = 24 if page_width < 400 else 28
    icon_size = 50

    return ft.SafeArea(
        top=True,
        left=False,
        right=False,
        content=ft.Container(
            width=float("inf"),
            height=100,
            bgcolor="#F5F5F5",
            padding=ft.padding.symmetric(horizontal=10),
            margin=0,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_color="#3EAEB1",
                        icon_size=icon_size,
                        on_click=on_back_click
                    ),
                    ft.Text(
                        titulo,
                        color="#3EAEB1",
                        size=text_size,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(width=icon_size)
                ]
            )
        )
    )



# ---------- VISTA GUARDADOS ----------
def render_guardados(page: ft.Page, cambiar_pantalla=None):
    page.clean()
    page.title = "Mis guardados"
    page.scroll = "auto"
    page.bgcolor = "white"
    page.padding = 0
    page.spacing = 0

    # ---------- INSTANCIAMOS EL MODAL ----------
    modal_reporte = ModalReporte(
        on_guardar=lambda desc: print(f" Reporte guardado: {desc}"),
        on_cancelar=lambda: print(" Reporte cancelado")
    )

    #  Lo agregamos al overlay para que siempre esté disponible
    if modal_reporte.dialog not in page.overlay:
        page.overlay.append(modal_reporte.dialog)

    # ---------- Card factory ----------
    def saved_card(nombre, categoria, subcategoria, precio, descripcion):
        if len(descripcion) > 300:
            descripcion = descripcion[:300] + "..."

        # Menú solo con Reportar (sin opción Guardar)
        menu_solo_reportar = menu_opciones(
            page, modal_reporte, text_color="black", incluir_guardar=False
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.CircleAvatar(radius=44, bgcolor="#E0E0E0"),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                nombre,
                                                size=18,
                                                weight="bold",
                                                color="teal"
                                            ),
                                            ft.Row(
                                                [
                                                    menu_solo_reportar,  # Menú de opciones
                                                    ft.IconButton(
                                                        icon=ft.Icons.DELETE_OUTLINE,  # Icono de bote de basura
                                                        icon_color="#3EAEB1",
                                                        icon_size=24,
                                                        on_click=lambda e: None  # solo visual
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                        ],
                                        alignment="spaceBetween",
                                        expand=True,
                                    ),

                                    ft.Row(
                                        [
                                            ft.Text(categoria, size=14, color="black", weight="bold"),
                                            ft.Text("·", size=14),
                                            ft.Text(subcategoria, size=14, color="#666666", weight="bold"),
                                        ],
                                        spacing=4,
                                    ),
                                    ft.Text(precio, size=13, weight="bold", color="#666666"),
                                    ft.Text(
                                        descripcion,
                                        size=13,
                                        color="black",
                                        no_wrap=False,
                                        weight="bold",
                                    ),
                                ],
                                spacing=3,
                                expand=True,
                            ),
                        ],
                        alignment="start",
                        spacing=12,
                    ),
                    ft.Row(
                        [
                            ft.Container(width=page.width * 0.25),  # Espacio vacío a la izquierda
                            ft.Container(
                                bgcolor="#DDDDDD",
                                height=1,
                                width=page.width * 0.8,
                            ),
                        ],
                        spacing=0,
                    )
                ],
                spacing=8,
            ),
            padding=10,
            margin=ft.margin.only(left=5, right=5),
        )

    # ---------- Example cards ----------
    cards = ft.Column(
        [
            saved_card(
                "Nestor Martinez",
                "Educación",
                "Tutorías en línea",
                "COP 30.000/h",
                "Este servicio de limpieza es ideal para mantener tu hogar u oficina impecable."
            ),
            saved_card(
                "Nestor Martinez",
                "Educación",
                "Tutorías en línea",
                "COP 30.000/h",
                "La organización de tu hogar o espacio de trabajo puede influir directamente en tu bienestar y productividad diaria."
            ),
        ],
        expand=True,
        spacing=0,
    )

    def obtener_token(page):
        return getattr(page, "session_token", None)

    # ---------- Navegación inferior ----------
    def on_bottom_nav_click(index):
        if index == 0:  # Inicio
            cambiar_pantalla("inicio")
        elif index == 1:  # Categorias
            cambiar_pantalla("categorias")
        elif index == 2:  # Mensajes
            token = obtener_token(page)
            if token:
                cambiar_pantalla("mensajes")
            else:
                print("Inicia sesion o registrate")
        elif index == 3:  # Guardados
            token = obtener_token(page)
            if token:
                cambiar_pantalla("guardados")
            else:
                print("Inicia sesion o registrate")
        elif index == 4:  # Menú
            token = obtener_token(page)
            if token:
                cambiar_pantalla("menu")
            else:
                print("Inicia sesion o registrate")

    # Barra inferior
    page.bottom_appbar = ft.BottomAppBar(
        content=menu_inferior(selected_index=3, on_bottom_nav_click=on_bottom_nav_click),
        bgcolor=ft.Colors.WHITE,
    )

    # ---------- Layout principal ----------
    page.add(
        ft.Column(
            [
                nav_superior(
                    page.width,
                    "Guardados",
                    on_back_click=lambda e: cambiar_pantalla("inicio") if cambiar_pantalla else None
                ),
                cards
            ],
            scroll="auto",
            expand=True,
        )
    )
    page.update()  #  aseguramos refresco de toda la UI
