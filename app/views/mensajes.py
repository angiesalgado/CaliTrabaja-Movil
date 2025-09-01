import flet as ft
from app.components.menu_inferior import menu_inferior
from app.components.nav import nav_bar

def pantalla_mensajes(page: ft.Page, cambiar_pantalla):

    def obtener_token(page):
        return  getattr(page, "session_token", None)


    # Limpiar la página
    page.controls.clear()
    page.bottom_appbar = None
    page.bgcolor = "#FFFFFF"
    page.padding = 0

    # índice seleccionado en el menú inferior -> "Mensajes"
    selected_index = 2

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

    # ---------- NAV SUPERIOR ----------
    nav = nav_bar(
        page,
        page.width,
        show_back=True,
        show_explora=True,
        on_back_click=lambda e: cambiar_pantalla("inicio")
    )

    # ---------- CONTENIDO PRINCIPAL ----------
    contenido = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Mensajes", size=22, weight=ft.FontWeight.BOLD, color="black"),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10, bottom=12),
            ),
            ft.Text(
                "Aquí se mostrarán los mensajes.",
                size=14,
                color="black54",
                text_align=ft.TextAlign.CENTER
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # ---------- LAYOUT COMPLETO ----------
    layout = ft.Column(
        controls=[
            nav,
            ft.Container(
                alignment=ft.alignment.top_center,
                expand=True,
                padding=ft.padding.symmetric(horizontal=10),
                content=contenido
            )
        ],
        expand=True
    )

    # ---------- MENÚ INFERIOR ----------
    menu = menu_inferior(selected_index, on_bottom_nav_click)
    page.bottom_appbar = ft.BottomAppBar(
        content=menu,
        bgcolor=ft.Colors.WHITE,
        elevation=0,
    )

    # ---------- AGREGAR AL PAGE ----------
    page.add(layout)
    page.update()