# login_view.py
import flet as ft
import re
from . import  Inicio
from app.components.nav import nav_bar
from app.API_services.iniciar_sesion import iniciar_sesion_api


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

    def mostrar_snackbar(mensaje, exito=True):
        """Muestra SnackBar con estilo uniforme"""
        sb = ft.SnackBar(
            content=ft.Text(
                mensaje,
                color="white",
                size=16,
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=ft.Colors.GREEN if exito else ft.Colors.RED,
            duration=3000,
        )
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def iniciar_sesion(e):
        email = email_field.value.strip()
        password = password_field.value.strip()

        # Validaciones antes de llamar la API
        if not email or not password:
            mostrar_snackbar("Por favor, complete todos los campos.", exito=False)
            return

        if not validar_email(email):
            mostrar_snackbar("El correo electrónico no es válido.", exito=False)
            return

        # Llamada a la API
        resultado = iniciar_sesion_api(email, password)

        if not resultado.get("success"):
            mensaje_error = resultado.get("message", "Error desconocido.")
            mostrar_snackbar(mensaje_error, exito=False)
        else:
            # Guardar token y mostrar éxito
            page.session_token = resultado.get("token")
            mostrar_snackbar("Inicio de sesión exitoso.", exito=True)

            # Cargar vista principal
            page.clean()
            Inicio.pantalla_inicio(page, cambiar_pantalla)

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
        cambiar_pantalla("recuperar_contrasena")

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
