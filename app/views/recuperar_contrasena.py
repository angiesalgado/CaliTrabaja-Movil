# recuperar_contrasena_view.py
import flet as ft
from app.components.nav import nav_bar
from app.API_services.enviar_correo_recu import enviar_correo_usu


# ---------- FUNCIÓN GLOBAL PARA MOSTRAR SNACKBAR ----------
def mostrar_snackbar(page: ft.Page, mensaje: str, exito=True):
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


def recuperar_contrasena(page: ft.Page, cambiar_pantalla):
    page.title = "Recuperar contraseña"
    max_content_width = 600

    email_field = ft.TextField(
        label="Correo electrónico",
        label_style=ft.TextStyle(font_family="OswaldBold", size=16, weight=ft.FontWeight.BOLD),
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#D9D9D9",
        expand=True
    )

    def enviar_link(e):
        correo = email_field.value.strip() if email_field.value else ""

        # Validar que no esté vacío
        if not correo:
            mostrar_snackbar(page, "Por favor ingresa un correo válido", exito=False)
            return

        # Validar formato básico de email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, correo):
            mostrar_snackbar(page, "El formato del correo no es válido", exito=False)
            return

        try:
            # Llamar al servicio para enviar el correo
            data = {'correo': correo}
            respuesta = enviar_correo_usu(data)

            # Verificar respuesta del servicio
            if respuesta and respuesta.get("success"):
                mostrar_snackbar(page, "Se ha enviado un enlace de recuperación a tu correo", exito=True)
                # Opcional: limpiar el campo después del envío exitoso
                email_field.value = ""
                email_field.update()
            elif respuesta and respuesta.get("error"):
                mostrar_snackbar(page, respuesta["error"], exito=False)
            else:
                mostrar_snackbar(page, "Error al enviar el correo. Intenta nuevamente", exito=False)

        except Exception as ex:
            print(f"Error al enviar correo de recuperación: {ex}")
            mostrar_snackbar(page, "Error de conexión. Verifica tu internet e intenta nuevamente", exito=False)

    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # NAV SUPERIOR
                nav_bar(
                    page,
                    page_width,
                    show_back=True,
                    on_back_click=lambda e: cambiar_pantalla("login")
                ),

                # Contenedor principal
                ft.Container(
                    width=container_width,
                    alignment=ft.alignment.center,
                    padding=20,
                    content=ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # --- Título ---
                            ft.Text(
                                "Recupera tu contraseña",
                                size=30,
                                color="#3EAEB1",
                                font_family="OswaldBold",
                                weight=ft.FontWeight.BOLD
                            ),
                            # --- Campo correo ---
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
                            # --- Texto descriptivo ---
                            ft.Text(
                                "Te enviaremos un enlace para restablecer tu contraseña",
                                size=16,
                                text_align=ft.TextAlign.CENTER,
                                font_family="OswaldBold",
                                weight=ft.FontWeight.BOLD
                            ),
                            # --- Botón enviar ---
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text(
                                        "Enviar",
                                        size=20,
                                        color="black",
                                        font_family="OswaldBold",
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    width=150,
                                    height=30,
                                    style=ft.ButtonStyle(
                                        bgcolor="#D9D9D9",
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=enviar_link
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