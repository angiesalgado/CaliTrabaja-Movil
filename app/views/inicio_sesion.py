# login_view.py
import flet as ft
import re
from app.components.nav import nav_bar


def inicio_sesion(page: ft.Page, cambiar_pantalla):
    page.title = "Inicio de sesión"
    max_content_width = 600

    # Campo de correo electrónico
    email_field = ft.TextField(
        label="Correo electrónico",
        label_style=ft.TextStyle(font_family="OswaldBold", size=16, weight=ft.FontWeight.BOLD),
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#D9D9D9",
        expand=True
    )

    # Campo de contraseña
    password_field = ft.TextField(
        label="Contraseña",
        label_style=ft.TextStyle(font_family="OswaldBold", size=16, weight=ft.FontWeight.BOLD),
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#D9D9D9",
        expand=True
    )
    message_text = ft.Text("", size=14, color="red", weight=ft.FontWeight.BOLD)

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
            title=ft.Text("Confirmar", weight=ft.FontWeight.BOLD),
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
            title=ft.Text("Recuperar contraseña", weight=ft.FontWeight.BOLD),
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
                            # --- Título ---
                            ft.Container(
                                padding=ft.padding.only(top=20),
                                content=ft.Text(
                                    "Iniciar sesión",
                                    size=30,
                                    color="#3EAEB1",
                                    font_family="OswaldBold",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),
                            # --- Correo ---
                            ft.Container(
                                bgcolor="#D9D9D9",
                                border_radius=8,
                                padding=ft.padding.only(left=12, right=8, top=5, bottom=5),
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(name="alternate_email", color="#3EAEB1"),
                                        email_field
                                    ]
                                )
                            ),
                            # --- Contraseña ---
                            ft.Container(
                                bgcolor="#D9D9D9",
                                border_radius=8,
                                padding=ft.padding.only(left=12, right=8, top=5, bottom=5),
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(name="lock", color="#3EAEB1"),
                                        password_field
                                    ]
                                )
                            ),
                            message_text,
                            # --- Botón Iniciar sesión ---
                            ft.Container(
                                padding=ft.padding.only(top=1),
                                content=ft.ElevatedButton(
                                    content=ft.Text(
                                        "Iniciar sesión",
                                        size=20,
                                        color="black",
                                        font_family="OswaldBold",
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    width=200,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        bgcolor="#D9D9D9",
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=iniciar_sesion
                                )
                            ),
                            # --- Links debajo (uno debajo del otro) ---
                            ft.Column(
                                spacing=5,  # 👈 cerca pero no pegados
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.TextButton(
                                        "¿Olvidaste tu contraseña?",
                                        on_click=olvidar_contrasena,
                                        style=ft.ButtonStyle(
                                            color="black",
                                            text_style=ft.TextStyle(
                                                font_family="OswaldBold",
                                                weight=ft.FontWeight.BOLD
                                            )
                                        )
                                    ),
                                    ft.TextButton(
                                        "Crear una cuenta",
                                        on_click=crear_cuenta,
                                        style=ft.ButtonStyle(
                                            color="black",
                                            text_style=ft.TextStyle(
                                                font_family="OswaldBold",
                                                weight=ft.FontWeight.BOLD
                                            )
                                        )
                                    )
                                ]
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
