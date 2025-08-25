import flet as ft

def nav_bar(page_width=None):
    text_size = 24 if page_width and page_width < 400 else 28

    return ft.Container(
        width=float("inf"),
        bgcolor="#F8F8F8",
        padding=ft.padding.only(top=40, bottom=20),
        content=ft.Stack(
            controls=[
                # 🔙 Botón de volver
                ft.Container(
                    left=10,
                    top=10,
                    content=ft.Icon(name="arrow_back_ios", color="#3EAEB1", size=28)
                ),
                # 🧠 Logo y texto centrados
                ft.Container(
                    alignment=ft.alignment.top_center,
                    content=ft.Row(
                        spacing=5,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(src="img.png", width=50),
                            ft.Row(
                                spacing=0,
                                controls=[
                                    ft.Text("Cali", color="#3EAEB1", size=text_size, font_family="OswaldBold"),
                                    ft.Text("Trabaja", color="black", size=text_size, font_family="OswaldBold")
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    )
