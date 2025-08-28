# app/components/nav_bar.py
import flet as ft

def nav_bar(page, page_width: float,
            show_back: bool = False,
            show_explora: bool = False,
            show_login_button: bool = False,   # 👈 nuevo parámetro
            on_back_click=None,
            on_login_click=None):
    text_size = 24 if page_width < 400 else 28
    back_action = on_back_click if on_back_click else (lambda e: page.go("/"))

    # ----------- Flecha izquierda -----------
    back_button = (
        ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS,
                icon_color="#3EAEB1",
                icon_size=28,
                on_click=back_action,
            ),
            padding=ft.padding.only(left=10),
        )
        if show_back else ft.Container(width=48)
    )

    # ----------- Logo + Texto -----------
    if show_explora:
        center_content = ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="img.png", width=50, height=50, fit=ft.ImageFit.CONTAIN),
                ft.Column(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Text("Explora en", size=text_size - 4, color="black", weight=ft.FontWeight.BOLD),
                        ft.Row(
                            spacing=0,
                            controls=[
                                ft.Text("Cali", color="#3EAEB1", size=text_size, weight=ft.FontWeight.BOLD),
                                ft.Text("Trabaja", color="black", size=text_size, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                    ],
                ),
            ],
        )
    else:
        center_content = ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="img.png", width=50),
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.Text("Cali", color="#3EAEB1", size=text_size, weight=ft.FontWeight.BOLD),
                        ft.Text("Trabaja", color="black", size=text_size, weight=ft.FontWeight.BOLD),
                    ]
                )
            ],
        )

    # ----------- Ícono de login (círculo de usuario) -----------
    login_icon = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
            icon_color="#3EAEB1",
            icon_size=40,
            on_click=lambda e: page.go("/login"),  # Redirige a /login
            tooltip="Iniciar sesión",
        ),
        padding=ft.padding.only(right=10),
    ) if show_login_button else None

    # ----------- Layout con Stack -----------
    stack_controls = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                back_button,
                ft.Container(content=center_content),
                ft.Container(width=48),
            ],
        )
    ]

    if login_icon:
        stack_controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[login_icon],
            )
        )

    return ft.Container(
        width=float("inf"),
        bgcolor="#F8F8F8",
        padding=ft.padding.only(top=30, bottom=40),
        content=ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=stack_controls
        ),
    )
