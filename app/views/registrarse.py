import flet as ft
import re
from app.API_services.registrar_usuario import registrar_usuario_api
from app.components.nav_bar import nav_bar
from . import Inicio

def pantalla_registro(page: ft.Page, cambiar_pantalla, origen=None):
    page.title = "Registrarse"
    page.scroll = "adaptive"
    max_content_width = 600
    campo_bgcolor = "#D9D9D9"

    # --- ESTILOS UNIFICADOS ---
    label_style = ft.TextStyle(font_family="OswaldBold", size=16, weight=ft.FontWeight.BOLD)
    input_style = ft.TextStyle(font_family="OswaldMedium", size=16, color="black")

    # --- CAMPOS ---
    nombre_field = ft.TextField(label="Primer nombre", label_style=label_style, text_style=input_style,
                                border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    apellido_field = ft.TextField(label="Primer apellido", label_style=label_style, text_style=input_style,
                                  border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    email_field = ft.TextField(label="Correo electrónico", label_style=label_style, text_style=input_style,
                               border=ft.InputBorder.NONE, filled=True, bgcolor=campo_bgcolor, expand=True)
    password_field = ft.TextField(label="Contraseña", label_style=label_style, text_style=input_style,
                                  password=True, can_reveal_password=True, border=ft.InputBorder.NONE,
                                  filled=True, bgcolor=campo_bgcolor, expand=True)
    confirm_field = ft.TextField(label="Repetir contraseña", label_style=label_style, text_style=input_style,
                                 password=True, can_reveal_password=True, border=ft.InputBorder.NONE,
                                 filled=True, bgcolor=campo_bgcolor, expand=True)

    message_text = ft.Text("", size=14, color="red", weight=ft.FontWeight.BOLD)

    # --- VALIDACIONES ---
    def validar_email(email):
        return "@" in email and "." in email

    def registrarse(e):
        if not all([nombre_field.value, apellido_field.value, email_field.value, password_field.value, confirm_field.value]):
            message_text.value = "Por favor, complete todos los campos."
        elif not validar_email(email_field.value):
            message_text.value = "Correo electrónico inválido."
        elif password_field.value != confirm_field.value:
            message_text.value = "Las contraseñas no coinciden."
        nombre = nombre_field.value
        apellido = apellido_field.value
        email = email_field.value
        password = password_field.value
        confirm = confirm_field.value
        resultado = registrar_usuario_api(nombre,apellido,email,password,confirm)
        if resultado.get("success")==False:
            message_text.value = resultado.get("message", "Error desconocido.")
        else:
            message_text.value = "✅ Registro exitoso (simulado)."
            page.session_token = resultado.get("token")
            page.clean()
            Inicio.pantalla_inicio(page,cambiar_pantalla)
        page.update()




    def ir_a_login(e):
        cambiar_pantalla("login")

    # --- WIDGET PARA AGRUPAR CAMPO CON ÍCONO ---
    def icon_text(icon_name, field):
        return ft.Container(
            bgcolor=campo_bgcolor,
            border_radius=8,
            padding=ft.padding.only(left=12, right=8, top=5, bottom=5),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(name=icon_name, size=28, color="#3EAEB1"),
                    field
                ]
            )
        )

    # --- UI ---
    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)
        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # NAV SUPERIOR
                nav_bar(
                    page,
                    page_width,
                    show_back=True,
                    on_back_click=lambda e: cambiar_pantalla(origen if origen else "login")
                ),

                ft.Container(
                    width=container_width,
                    alignment=ft.alignment.center,
                    padding=20,
                    content=ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # --- TÍTULO ---
                            ft.Container(
                                padding=ft.padding.only(top=20),
                                content=ft.Text(
                                    "Registrarse",
                                    size=30,
                                    color="#3EAEB1",
                                    font_family="OswaldBold",
                                    weight=ft.FontWeight.BOLD
                                )
                            ),
                            # --- CAMPOS ---
                            icon_text("person", nombre_field),
                            icon_text("person", apellido_field),
                            icon_text("alternate_email", email_field),
                            icon_text("lock", password_field),
                            icon_text("lock", confirm_field),
                            message_text,
                            # --- BOTÓN REGISTRO ---
                            ft.Container(
                                padding=ft.padding.only(top=1),
                                content=ft.ElevatedButton(
                                    content=ft.Text(
                                        "Registrarse",
                                        size=20,
                                        color="black",
                                        font_family="OswaldBold",
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    width=200,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        bgcolor=campo_bgcolor,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=registrarse
                                )
                            ),
                            # --- LINK LOGIN ---
                            ft.TextButton(
                                "¿Ya tienes una cuenta?",
                                on_click=ir_a_login,
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
