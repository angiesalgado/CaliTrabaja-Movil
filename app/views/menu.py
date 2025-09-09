import flet as ft
from app.components.nav import nav_bar
from app.components.menu_inferior import menu_inferior
from app.views import configuracion
from app.API_services.cerrar_sesion import cerrar_sesion_api
from . import Inicio


def pantalla_menu(page: ft.Page, cambiar_pantalla):
    page.controls.clear()
    page.bottom_appbar = None
    page.update()

    selected_side_index = ft.Ref[int]()
    selected_side_index.value = -1

    selected_bottom_index = ft.Ref[int]()
    selected_bottom_index.value = 4  # Menú seleccionado por defecto


    def obtener_token(page):
        return getattr(page, "session_token", None)

    token = obtener_token(page)

    # Construye dinámicamente los ítems del menú lateral
    def get_side_menu_items():
        items = [
            {"icon": ft.Icons.HOME_OUTLINED, "text": "Inicio"},
            {"icon": ft.Icons.GRID_VIEW, "text": "Publicaciones"},
        ]
        if token:
            items.append({"icon": ft.Icons.SETTINGS, "text": "Configuración"})
            items.append({"icon": "logout", "text": "Cerrar sesión"})
        return items

    # Usa esto en vez de la lista fija
    side_menu_items = get_side_menu_items()

    def mostrar_snackbar(mensaje, exito=True):
        """Muestra SnackBar con estilo uniforme"""
        sb = ft.SnackBar(
            content=ft.Text(
                mensaje,
                color="white",
                size=16,
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=ft.Colors.GREEN if exito else ft.Colors.RED,
            duration=3000,
        )
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def on_side_nav_click(index):
        selected_side_index.value = index
        selected_bottom_index.value = -1

        item_text = side_menu_items[index]["text"]

        if item_text == "Inicio":
            cambiar_pantalla("inicio")
        elif item_text == "Publicaciones":
            cambiar_pantalla("publicaciones")
        elif item_text == "Configuración":
            configuracion.pantalla_configuracion(page, cambiar_pantalla)
        elif item_text == "Cerrar sesión":
            cerrar_sesion_api(token)
            page.session_token = None
            mostrar_snackbar("Sesión cerrada correctamente.", exito=True)
            page.clean()
            Inicio.pantalla_inicio(page, cambiar_pantalla)

        build_side_menu()
        update_bottom_bar()
        page.update()


    def on_bottom_nav_click(index):
        selected_bottom_index.value = index
        selected_side_index.value = -1

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
            cambiar_pantalla("menu")



        build_side_menu()
        update_bottom_bar()
        page.update()

    # Construcción menú lateral
    side_menu = ft.Column(width=200, spacing=0)

    def build_side_menu_item(index, item):
        selected = index == selected_side_index.value
        color = "#3EAEB1" if selected else ft.Colors.BLACK
        icon = ft.Icon(item["icon"], color=color, size=24) if isinstance(item["icon"], str) \
            else ft.Icon(item["icon"], color=color, size=24)

        return ft.Container(
            content=ft.Row(
                [
                    icon,
                    ft.Text(item["text"], size=16, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(vertical=15, horizontal=20),
            on_click=lambda e, idx=index: on_side_nav_click(idx),
            ink=True,
        )

    def build_side_menu():
        side_menu.controls.clear()
        for i, item in enumerate(side_menu_items):
            side_menu.controls.append(build_side_menu_item(i, item))

    build_side_menu()

    # Contenido principal vacío por ahora
    contenido = ft.Container(expand=True)

    # Menú inferior dinámico
    bottom_bar_container = menu_inferior(selected_bottom_index.value, on_bottom_nav_click)

    def update_bottom_bar():
        bottom_bar_container.content.controls.clear()
        bottom_bar_container.content.controls.extend(
            menu_inferior(selected_bottom_index.value, on_bottom_nav_click).content.controls
        )

    # Barra superior nav3 con botón de volver (este sí va al inicio)
    nav = nav_bar(page, page.width, show_back=True, show_explora=True,
                  on_back_click=lambda e: cambiar_pantalla("inicio"))
    # Estructura general
    layout = ft.Column(
        controls=[
            nav,
            ft.Row(
                controls=[
                    side_menu,
                    contenido
                ],
                expand=True
            )
        ],
        expand=True
    )

    page.bottom_appbar = ft.BottomAppBar(
        content=bottom_bar_container,
        bgcolor=ft.Colors.WHITE,
        elevation=0
    )

    page.add(layout)
    page.update()
