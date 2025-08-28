import flet as ft
from app.components.nav_bar import nav_bar

def recuperar_contrasena(page: ft.Page, cambiar_pantalla):
    page.title = "Recuperar contraseña"
    max_content_width = 600
    campo_bgcolor = "#D9D9D9"

    email_field = ft.TextField(
        label="Correo electrónico",
        label_style=ft.TextStyle(font_family="OswaldBold", size=16, weight="bold"),
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor=campo_bgcolor,
        expand=True
    )

    message_text = ft.Text("", size=14, color="red")

    def enviar_correo(e):
        email = email_field.value.strip()
        if not email:
            message_text.value = "Por favor, ingresa tu correo electrónico."
        else:
            message_text.value = "Se ha enviado un enlace para restablecer tu contraseña (simulado)."
        page.update()

    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)

        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                nav_bar(page, page_width, show_back=True, on_back_click=lambda e: cambiar_pantalla("login")),
                ft.Container(
                    width=container_width,
                    alignment=ft.alignment.center,
                    padding=20,
                    content=ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=ft.padding.only(top=40),
                                content=ft.Text("Recupera tu contraseña", size=32, color="#3EAEB1", font_family="OswaldBold", weight="bold")
                            ),
                            ft.Container(
                                bgcolor=campo_bgcolor,
                                border_radius=8,
                                padding=5,
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            padding=ft.padding.only(left=10),
                                            content=ft.Icon(name="alternate_email", color="#3EAEB1")
                                        ),
                                        email_field
                                    ]
                                )
                            ),
                            ft.Text(
                                "Te enviaremos un enlace para restablecer tu contraseña",
                                text_align="center",
                                font_family="OswaldBold"
                            ),
                            message_text,
                            ft.Container(
                                padding=ft.padding.only(top=20),
                                content=ft.ElevatedButton(
                                    content=ft.Text("Enviar", size=20, color="black", font_family="OswaldBold", weight="bold"),
                                    width=160,
                                    style=ft.ButtonStyle(
                                        bgcolor=campo_bgcolor,
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=enviar_correo
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def on_resize(e):
        page.controls.clear()
        page.controls.append(
            ft.Container(
                content=build_content(page.width),
                alignment=ft.alignment.top_center,
                expand=True
            )
        )
        page.update()

    page.on_resize = on_resize
    on_resize(None)
