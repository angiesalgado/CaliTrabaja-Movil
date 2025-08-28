import flet as ft
import re
from app.components.nav_bar import nav_bar

def pantalla_registro(page: ft.Page, cambiar_pantalla, origen=None):
    page.title = "Registrarse"
    max_content_width = 600
    campo_bgcolor = "#D9D9D9"
    label_style = ft.TextStyle(font_family="OswaldBold", size=16, weight="bold")

    # Campos de entrada
    nombre_field = ft.TextField(label="Primer nombre", label_style=label_style, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    apellido_field = ft.TextField(label="Primer apellido", label_style=label_style, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    email_field = ft.TextField(label="Correo electrónico", label_style=label_style, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    password_field = ft.TextField(label="Contraseña", label_style=label_style, password=True, can_reveal_password=True, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    confirm_field = ft.TextField(label="Repetir contraseña", label_style=label_style, password=True, can_reveal_password=True, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)

    message_text = ft.Text("", size=14, color="red")

    def validar_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def registrarse(e):
        if not all([nombre_field.value, apellido_field.value, email_field.value, password_field.value, confirm_field.value]):
            message_text.value = "Por favor, complete todos los campos."
        elif not validar_email(email_field.value):
            message_text.value = "Correo electrónico inválido."
        elif password_field.value != confirm_field.value:
            message_text.value = "Las contraseñas no coinciden."
        else:
            message_text.value = "✅ Registro exitoso (simulado)."
        page.update()

    def ir_a_login(e):
        cambiar_pantalla("login")

    def build_input(icon_name, field):
        return ft.Container(
            bgcolor=campo_bgcolor,
            border_radius=8,
            padding=5,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=10),
                        content=ft.Icon(name=icon_name, color="#3EAEB1")
                    ),
                    field
                ]
            )
        )

    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)

        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                nav_bar(page, page_width, show_back=True, on_back_click=lambda e: cambiar_pantalla(origen if origen else "login")),
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
                                content=ft.Text("Registrarse", size=32, color="#3EAEB1", font_family="OswaldBold", weight="bold")
                            ),
                            build_input("person_outline", nombre_field),
                            build_input("person_outline", apellido_field),
                            build_input("alternate_email", email_field),
                            build_input("lock", password_field),
                            build_input("lock", confirm_field),
                            message_text,
                            ft.Container(
                                padding=ft.padding.only(top=20),
                                content=ft.ElevatedButton(
                                    content=ft.Text("Registrarse", size=20, color="black", font_family="OswaldBold", weight="bold"),
                                    width=160,
                                    style=ft.ButtonStyle(bgcolor=campo_bgcolor, shape=ft.RoundedRectangleBorder(radius=8)),
                                    on_click=registrarse
                                )
                            ),
                            ft.TextButton(
                                content=ft.Text("¿Ya tienes una cuenta?", font_family="OswaldBold", weight="bold", color="black"),
                                on_click=ir_a_login
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
