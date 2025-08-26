import flet as ft
from app.components.menu_inferior import menu_inferior

# ---------- NAV SUPERIOR DE CONFIGURACIÓN ----------
def nav_configuracion(page: ft.Page, page_width: float, titulo="Configuración", cambiar_pantalla=None):
    text_size = 24 if page_width < 400 else 28
    icon_size = 50

    def volver_menu(e):
        print("DEBUG: clic en flecha atrás")
        if cambiar_pantalla:
            print("DEBUG: usando cambiar_pantalla('menu')")
            cambiar_pantalla("menu")
        else:
            print("DEBUG: usando page.go('/menu')")
            page.go("/menu")

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
                        on_click=volver_menu
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


# ---------- PANTALLA PRINCIPAL DE CONFIGURACIÓN ----------
def pantalla_configuracion(page: ft.Page, cambiar_pantalla=None):
    usuario_nombre = "Angie"
    usuario_rol = "Cliente"
    usuario_fecha_union = "12/08/2024"

    # Ajustes base de página
    page.controls.clear()
    page.bottom_appbar = None
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.spacing = 0

    # ---------- FACTORÍA CAMPOS PASSWORD ----------
    def password_field_factory():
        field = ft.TextField(
            password=True,
            can_reveal_password=False,
            width=400,
            height=50,
            bgcolor="#E0E0E0",
            border_radius=8,
            border_color="transparent",
            text_style=ft.TextStyle(color=ft.Colors.BLACK, size=16),
            cursor_color=ft.Colors.BLACK,
            selection_color="#B0BEC5",
        )
        toggle_btn = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF)

        def toggle_password(e):
            field.password = not field.password
            toggle_btn.icon = ft.Icons.VISIBILITY if not field.password else ft.Icons.VISIBILITY_OFF
            field.update()
            toggle_btn.update()

        toggle_btn.on_click = toggle_password
        field.suffix = toggle_btn
        return field

    # ---------- NAV INFERIOR (usa cambiar_pantalla) ----------
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

    # ---------- SUBVISTAS ----------
    def cambiar_contrasena():
        page.controls.clear()
        page.bottom_appbar = None
        actual_field = password_field_factory()
        nueva_field = password_field_factory()
        repetir_field = password_field_factory()

        page.add(
            ft.Column(
                controls=[

                    ft.Container(
                        width=float("inf"),
                        bgcolor="#FFFFFF",
                        padding=ft.padding.symmetric(horizontal=20, vertical=30),
                        content=ft.Column(
                            spacing=20,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.START if page.width < 500 else ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[
                                ft.Text("Cambiar contraseña", size=22, weight=ft.FontWeight.BOLD, color="#3EAEB1"),
                                ft.Text("Contraseña actual", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                actual_field,
                                ft.Text("Nueva contraseña", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                nueva_field,
                                ft.Text("Repetir contraseña", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                repetir_field,
                                ft.Row(
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Guardar cambios",
                                            bgcolor="#3EAEB1",
                                            color="white",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                        ),
                                        ft.ElevatedButton(
                                            "Cancelar",
                                            bgcolor="#F2F2F2",
                                            color="black",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                            on_click=lambda e: mostrar_configuracion()
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        page.update()

    def eliminar_cuenta():
        page.controls.clear()
        page.bottom_appbar = None
        confirmar_field = password_field_factory()

        page.add(
            ft.Column(
                controls=[

                    ft.Container(
                        width=float("inf"),
                        bgcolor="#FFFFFF",
                        padding=ft.padding.symmetric(horizontal=20, vertical=30),
                        content=ft.Column(
                            spacing=20,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.START if page.width < 500 else ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[
                                ft.Text("Deshabilitar cuenta", size=22, weight=ft.FontWeight.BOLD, color="#3EAEB1"),
                                ft.Text(
                                    "Esta acción es permanente y no se puede deshacer.\n"
                                    "Toda tu información se eliminará de forma irreversible.\n"
                                    "No podrás volver a iniciar sesión con esta cuenta.",
                                    size=16,
                                    color="#000000"
                                ),
                                ft.Text("Confirmar contraseña", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                confirmar_field,
                                ft.Row(
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Deshabilitar cuenta",
                                            bgcolor="#3EAEB1",
                                            color="white",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                        ),
                                        ft.ElevatedButton(
                                            "Cancelar",
                                            bgcolor="#F2F2F2",
                                            color="black",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                            on_click=lambda e: mostrar_configuracion()
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        page.update()

    # ---------- VISTA PRINCIPAL DE CONFIGURACIÓN ----------
    def mostrar_configuracion():
        page.controls.clear()

        # Barra superior con flecha que vuelve al MENÚ
        header = nav_configuracion(page, page.width, "Configuración", cambiar_pantalla)

        contenido = ft.Container(
            expand=True,
            width=float("inf"),
            bgcolor="#FFFFFF",
            padding=16,
            margin=ft.margin.only(top=30),
            content=ft.Column(
                scroll="auto",
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=40),
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Nombre del usuario:", size=16,
                                                weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Text(usuario_nombre, size=16, color="#000000")
                                    ],
                                    spacing=5
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Rol actual:", size=16,
                                                weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Text(usuario_rol, size=16, color="#000000")
                                    ],
                                    spacing=5
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Se unió en:", size=16,
                                                weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Text(usuario_fecha_union, size=16, color="#000000")
                                    ],
                                    spacing=5
                                )
                            ]
                        )
                    ),
                    ft.Divider(thickness=1, color="#000000"),
                    ft.ListTile(
                        content_padding=ft.padding.only(left=40, right=10),
                        title=ft.Text("Cambiar contraseña", color="#000000",
                                      weight=ft.FontWeight.BOLD, size=16),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#3EAEB1"),
                        on_click=lambda e: cambiar_contrasena()
                    ),
                    ft.Divider(thickness=1, color="#000000"),
                    ft.ListTile(
                        content_padding=ft.padding.only(left=40, right=10),
                        title=ft.Text("Eliminar cuenta", color="#000000",
                                      weight=ft.FontWeight.BOLD, size=16),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#3EAEB1"),
                        on_click=lambda e: eliminar_cuenta()
                    ),
                    ft.Divider(thickness=1, color="#000000"),
                ]
            )
        )

        # Layout principal
        page.add(
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[header, contenido]
                    )
                ]
            )
        )


        page.bottom_appbar = ft.BottomAppBar(
            content=menu_inferior(
                selected_index=4,                # resalta "Menú" como activo
                on_bottom_nav_click=on_bottom_nav_click
            ),
            bgcolor=ft.Colors.WHITE,
            elevation=0
        )

        page.update()

    # -------- INICIO --------
    mostrar_configuracion()
