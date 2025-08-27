import flet as ft
import re
from app.components.nav_bar import nav_bar

def pantalla_registro(page: ft.Page, cambiar_pantalla, origen=None):
    page.title = "Registrarse"
    page.scroll = "adaptive"
    max_content_width = 600
    campo_bgcolor = "#D9D9D9"

    label_style = ft.TextStyle(font_family="OswaldBold", size=16)
    text_style = ft.TextStyle(font_family="OswaldMedium", color=ft.Colors.BLACK)

    # Campos de entrada
    nombre_field = ft.TextField(label="Primer nombre", label_style=label_style, text_style=text_style, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    apellido_field = ft.TextField(label="Primer apellido", label_style=label_style, text_style=text_style, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    email_field = ft.TextField(label="Correo electrónico", label_style=label_style, text_style=text_style, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    password_field = ft.TextField(label="Contraseña", label_style=label_style, text_style=text_style, password=True, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    confirm_field = ft.TextField(label="Repetir contraseña", label_style=label_style, text_style=text_style, password=True, border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)

    message_text = ft.Text("", size=14, color="red")

    def validar_email(email):
        return "@" in email and "." in email

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

    def password_toggle_factory(field):
        visible = {"value": False}
        def toggle_visibility(e):
            visible["value"] = not visible["value"]
            field.password = not visible["value"]
            icon_button.icon = ft.Icons.VISIBILITY if visible["value"] else ft.Icons.VISIBILITY_OFF
            field.update()
            icon_button.update()
        icon_button = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            icon_color="#3EAEB1",
            icon_size=28,
            tooltip="Mostrar/Ocultar",
            style=ft.ButtonStyle(bgcolor=campo_bgcolor, padding=10),
            on_click=toggle_visibility
        )
        return icon_button

    password_toggle = password_toggle_factory(password_field)
    confirm_toggle = password_toggle_factory(confirm_field)

    def icon_text(icon_name, field, extra=None):
        controls = [ft.Icon(name=icon_name, size=28, color="#3EAEB1"), field]
        if extra:
            controls.append(extra)
        return ft.Container(
            bgcolor=campo_bgcolor,
            border_radius=8,
            padding=5,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=controls
            )
        )

    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)
        return ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # ---------------- NAV SUPERIOR ----------------
                nav_bar(
                    page,
                    page_width,
                    show_back=True,
                    on_back_click=lambda e: cambiar_pantalla(origen if origen else "login")
                ),

                ft.Container(
                    width=container_width,  # <-- AÑADE ESTO
                    padding=ft.padding.only(top=40),
                    content=ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Registrarse", size=28, color="#3EAEB1", font_family="OswaldBold"),
                            icon_text(ft.Icons.PERSON_OUTLINE, nombre_field),
                            icon_text(ft.Icons.PERSON_OUTLINE, apellido_field),
                            icon_text(ft.Icons.ALTERNATE_EMAIL, email_field),
                            icon_text(ft.Icons.LOCK_OUTLINE, password_field, password_toggle),
                            icon_text(ft.Icons.LOCK_OUTLINE, confirm_field, confirm_toggle),
                            message_text,
                            ft.Container(
                                padding=ft.padding.only(top=20),
                                content=ft.ElevatedButton(
                                    content=ft.Text("Registrarse", size=20, color="black", font_family="OswaldMedium"),
                                    width=160,
                                    style=ft.ButtonStyle(bgcolor=campo_bgcolor,
                                                         shape=ft.RoundedRectangleBorder(radius=8)),
                                    on_click=registrarse
                                )
                            ),
                            ft.TextButton(
                                content=ft.Text("¿Ya tienes una cuenta?",
                                                style=ft.TextStyle(font_family="OswaldMedium")),
                                on_click=ir_a_login,
                                style=ft.ButtonStyle(overlay_color="transparent", bgcolor="transparent")
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
                expand=True,
                padding=0
            )
        )
        page.update()

    page.on_resize = on_resize
    on_resize(None)
