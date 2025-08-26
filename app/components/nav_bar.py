import flet as ft

def nav_bar(page, page_width: float, show_back: bool = False, show_explora: bool = False, on_back_click=None):
    text_size = 24 if page_width < 400 else 28

    # Acción por defecto del back
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
            padding=ft.padding.only(left=10),  # 👈 leve separación al borde
        )
        if show_back else ft.Container(width=48)  # espacio reservado si no hay flecha
    )

    # ----------- Logo + Texto centrados -----------
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
                            spacing=0,  # 👈 SIN espacio extra entre Cali y Trabaja
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
            spacing=8,  # espacio fijo entre logo y texto
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="img.png", width=50),
                ft.Row(  # 👈 metemos "Cali" + "Trabaja" juntos
                    spacing=0,
                    controls=[
                        ft.Text("Cali", color="#3EAEB1", size=text_size, weight=ft.FontWeight.BOLD),
                        ft.Text("Trabaja", color="black", size=text_size, weight=ft.FontWeight.BOLD),
                    ]
                )
            ],
        )

    # ----------- Layout 3 columnas (flecha | centro | espaciador) -----------
    return ft.Container(
        width=float("inf"),
        bgcolor="#F8F8F8",
        padding=ft.padding.only(top=30, bottom=20),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                back_button,                          # izquierda
                ft.Container(content=center_content), # centro
                ft.Container(width=48),               # derecha (espaciador para balancear)
            ],
        ),
    )
