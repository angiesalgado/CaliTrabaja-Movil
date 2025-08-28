# login_view.py
import flet as ft
import re
from app.components.nav_bar import nav_bar


def inicio_sesion(page: ft.Page, cambiar_pantalla):
    page.title = "Inicio de sesión"
    max_content_width = 600

    # Campo de correo electrónico
    email_field = ft.TextField(
        label="Correo electrónico",
        label_style=ft.TextStyle(font_family="OswaldBold", size=16),
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#D9D9D9",
        expand=True
    )

    # Campo de contraseña
    password_field = ft.TextField(
        label="Contraseña",
        label_style=ft.TextStyle(font_family="OswaldBold", size=16),
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#D9D9D9",
        expand=True
    )
    message_text = ft.Text("", size=14, color="red")

    def validar_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def iniciar_sesion(e):
        email = email_field.value.strip()
        password = password_field.value.strip()

        if not email or not password:
            message_text.value = "Por favor, complete todos los campos."
        elif not validar_email(email):
            message_text.value = "El correo electrónico no es válido."
        else:
            message_text.value = "Inicio de sesión exitoso (simulado)."
        page.update()

    def volver_atras(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Quieres salir de la pantalla de inicio de sesión?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.dialog.close()),
                ft.TextButton("Salir", on_click=lambda e: page.window_close())
            ]
        )
        page.dialog.open = True
        page.update()

    def olvidar_contrasena(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Recuperar contraseña"),
            content=ft.Text("Aquí iría el proceso para recuperar la contraseña."),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()

    def crear_cuenta(e):
        cambiar_pantalla("registro")

    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)
        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # ---------------- NAV SUPERIOR ----------------
                nav_bar(
                    page,
                    page_width,
                    show_back=True,
                    on_back_click=lambda e: cambiar_pantalla("inicio")
                ),

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
                                content=ft.Text(
                                    "Iniciar sesión",
                                    size=28,
                                    color="#3EAEB1",
                                    font_family="OswaldBold"
                                )
                            ),
                            ft.Container(
                                bgcolor="#D9D9D9",
                                border_radius=8,
                                padding=5,
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[ft.Icon(name="alternate_email", color="#3EAEB1"), email_field]
                                )
                            ),
                            ft.Container(
                                bgcolor="#D9D9D9",
                                border_radius=8,
                                padding=5,
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[ft.Icon(name="lock", color="#3EAEB1"), password_field]
                                )
                            ),
                            message_text,
                            ft.Container(
                                padding=ft.padding.only(top=20),
                                content=ft.ElevatedButton(
                                    content=ft.Text("Iniciar sesión", size=20, color="black", font_family="OswaldMedium"),
                                    width=160,
                                    style=ft.ButtonStyle(bgcolor="#D9D9D9", shape=ft.RoundedRectangleBorder(radius=8)),
                                    on_click=iniciar_sesion
                                )
                            ),
                            ft.TextButton("¿Olvidaste tu contraseña?", on_click=olvidar_contrasena),
                            ft.TextButton(
                                "Crear una cuenta",
                                on_click=crear_cuenta,
                                style=ft.ButtonStyle(text_style=ft.TextStyle(font_family="OswaldMedium"))
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
