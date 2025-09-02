import flet as ft
from app.components.nav import nav_bar
from app.components.menu_inferior import menu_inferior

def pantalla_categorias(page: ft.Page, cambiar_pantalla):
    page.controls.clear()
    page.bottom_appbar = None
    page.bgcolor = "#FFFFFF"
    page.padding = 0

    # Detectar si está en un dispositivo grande (PC)
    is_desktop = page.width >= 700
    max_content_width = 600 if is_desktop else 430
    item_spacing = 30 if is_desktop else 20

    def obtener_token(page):
        return getattr(page, "session_token", None)

    categorias = [
        ("tecnico.svg", "Reparación y\nmantenimiento", 1),
        ("cuidado.svg", "Cuidado y\nAsistencia", 2),
        ("mascoteros.svg", "Bienestar de\nmascotas", 3),
        ("educativos.svg", "Educativos y\naprendizaje", 4),
        ("limpieza.svg", "Hogar y\nlimpieza", 5),
        ("construccion.png", "Construcción y\nRemodelación", 6),
        ("artisticos.svg", "Artísticos y\ncreatividad", 7),
        ("transporte.svg", "Movilidad y\ntransporte", 8),
        ("culinarios.svg", "Gastronomía", 9),
        ("salud_bien.svg", "Bienestar\nPersonal", 10),
        ("eventos.svg", "Eventos", 11)
    ]

    def crear_categoria(imagen, texto, id_categoria):

        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Container(
                        width=100,
                        height=100,
                        bgcolor="#FFFFFF",
                        border=ft.border.all(1, "#000000"),
                        border_radius=10,
                        padding=8,
                        content=ft.Image(
                            src=imagen,
                            width=55,
                            height=55,
                            fit=ft.ImageFit.CONTAIN
                        ),
                    ),
                    ft.Text(
                        texto,
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                        color="black"
                    )
                ]
            ),
            # 👉 Al hacer clic en cualquier categoría va a publicaciones con origen=categorias
            on_click=lambda e, cat_id = id_categoria: cambiar_pantalla("publicaciones", origen={"categoria_id": cat_id} )
        )

    # Agrupar categorías en filas de a 3
    filas = []
    fila = []

    for i, (imagen, texto, id_categoria) in enumerate(categorias):
        fila.append(crear_categoria(imagen, texto,id_categoria,))
        if len(fila) == 3 or i == len(categorias) - 1:
            while len(fila) < 3:
                fila.append(ft.Container(width=100, height=100))  # espacio vacío
            filas.append(
                ft.Row(
                    controls=fila.copy(),
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=item_spacing
                )
            )
            fila = []

    # Este índice representa "Categorías"
    selected_index = 1

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
                cambiar_pantalla("menu")


    nav = nav_bar(
        page,
        page.width,
        show_back=True,
        show_explora=True,
        on_back_click=lambda e: cambiar_pantalla("inicio")
    )
    menu = menu_inferior(selected_index, on_bottom_nav_click)

    contenido = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Categorías", size=22, weight=ft.FontWeight.BOLD, color="black"),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10, bottom=12),
            ),
            *filas
        ],
        spacing=18,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    layout = ft.Column(
        controls=[
            nav,
            ft.Container(
                alignment=ft.alignment.top_center,
                expand=True,
                padding=ft.padding.symmetric(horizontal=10),
                content=ft.Container(
                    width=max_content_width,
                    content=contenido
                )
            )
        ],
        expand=True
    )

    page.bottom_appbar = ft.BottomAppBar(
        content=menu,
        bgcolor=ft.Colors.WHITE,
        elevation=0,
    )

    page.add(layout)
    page.update()
