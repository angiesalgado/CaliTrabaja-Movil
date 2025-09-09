import flet as ft
import re
from app.API_services.registrar_usuario import registrar_usuario_api
from app.components.nav import nav_bar
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

    # --- VALIDACIONES DE CONTRASEÑA ---
    regla_6_icon = ft.Icon(name=ft.Icons.HIGHLIGHT_OFF, color="red", size=18)
    regla_6_text = ft.Text("Al menos 6 caracteres", size=14)

    regla_mayus_icon = ft.Icon(name=ft.Icons.HIGHLIGHT_OFF, color="red", size=18)
    regla_mayus_text = ft.Text("Al menos 1 letra mayúscula", size=14)

    reglas_columna = ft.Column(
        spacing=5,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Row([regla_6_icon, regla_6_text], alignment=ft.MainAxisAlignment.START),
            ft.Row([regla_mayus_icon, regla_mayus_text], alignment=ft.MainAxisAlignment.START),
        ]
    )

    def validar_password(e=None):
        pwd = password_field.value or ""

        # Validar longitud
        if len(pwd) >= 6:
            regla_6_icon.name = ft.Icons.CHECK_CIRCLE
            regla_6_icon.color = "green"
        else:
            regla_6_icon.name = ft.Icons.HIGHLIGHT_OFF
            regla_6_icon.color = "red"

        # Validar mayúscula
        if re.search(r"[A-Z]", pwd):
            regla_mayus_icon.name = ft.Icons.CHECK_CIRCLE
            regla_mayus_icon.color = "green"
        else:
            regla_mayus_icon.name = ft.Icons.HIGHLIGHT_OFF
            regla_mayus_icon.color = "red"

        page.update()

    # Escuchar cambios en el campo contraseña
    password_field.on_change = validar_password

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

    def registrarse(e):
        if not all([nombre_field.value, apellido_field.value, email_field.value, password_field.value,
                    confirm_field.value]):
            mostrar_snackbar("Por favor, complete todos los campos.", exito=False)
            return
        elif not validar_email(email_field.value):
            mostrar_snackbar("Correo electrónico inválido.", exito=False)
            return
        elif password_field.value != confirm_field.value:
            mostrar_snackbar("Las contraseñas no coinciden.", exito=False)
            return

        nombre = nombre_field.value
        apellido = apellido_field.value
        email = email_field.value
        password = password_field.value
        confirm = confirm_field.value

        resultado = registrar_usuario_api(nombre, apellido, email, password, confirm)

        if resultado.get("success") == False:
            mostrar_snackbar(resultado.get("message", "Error desconocido."), exito=False)
        else:
            page.session_token = resultado.get("token")
            mostrar_snackbar("Registro exitoso.", exito=True)

            # Cargar pantalla de inicio
            page.clean()
            Inicio.pantalla_inicio(page, cambiar_pantalla)

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
                            # --- Contraseña ---
                            icon_text("lock", password_field),
                            reglas_columna,
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
