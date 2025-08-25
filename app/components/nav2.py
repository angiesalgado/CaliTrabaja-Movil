import flet as ft

def nav2_bar(page_width: float, search_ref=None):
    text_size = 24 if page_width < 400 else 28
    is_small_screen = page_width < 300

    return ft.Container(
        width=float("inf"),
        height=100,
        bgcolor="#F8F8F8",
        padding=ft.padding.only(top=40, bottom=20),
        margin=0,
        content=ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # ---------- Logo ----------
                ft.Row(
                    alignment=ft.MainAxisAlignment.START if is_small_screen else ft.MainAxisAlignment.CENTER,
                    spacing=5,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src="img.png", width=50),
                        ft.Row(
                            spacing=0,
                            controls=[
                                ft.Text("Cali", color="#3EAEB1", size=text_size, weight=ft.FontWeight.BOLD),
                                ft.Text("Trabaja", color="black", size=text_size, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                    ],
                ),


            ]
        )
    )
