import flet as ft

def nav3_bar(page_width: float, on_back_click=None):
    is_mobile = page_width < 500
    top_padding = 20 if is_mobile else 30
    icon_size = 50
    text_size = 24 if page_width < 400 else 28

    return ft.Container(
        bgcolor="#F5F5F5",
        padding=ft.padding.only(top=top_padding, left=12, right=12, bottom=12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Icono de retroceso
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    icon_color="#3EAEB1",
                    icon_size=icon_size,
                    on_click=on_back_click
                ),
                # Logo + texto en columna
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(  # Aquí bajamos un poco el logo
                            margin=ft.margin.only(top=12),
                            content=ft.Image(
                                src="img.png",
                                width=50,
                                height=50,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                        ),
                        ft.Column(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Explora en", size=text_size, color="black", weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Cali", color="#3EAEB1", size=text_size, weight=ft.FontWeight.BOLD),
                                        ft.Text("Trabaja", color="black", size=text_size, weight=ft.FontWeight.BOLD),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                ft.Container(width=icon_size),  # Espaciador
            ]
        )
    )
