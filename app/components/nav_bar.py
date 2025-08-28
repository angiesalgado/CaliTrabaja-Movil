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

    # ----------- Botón sobresalido -----------
    login_button = ft.Container(
        content=ft.ElevatedButton(
            "Iniciar sesión",
            bgcolor="#3EAEB1",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            on_click=on_login_click,
        ),
        right=10,
        bottom=-52,
    ) if show_login_button else None   # 👈 solo si lo piden

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

    if login_button:
        stack_controls.append(login_button)

    return ft.Container(
        width=float("inf"),
        bgcolor="#F8F8F8",
        padding=ft.padding.only(top=30, bottom=40),
        content=ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=stack_controls
        ),
    )
