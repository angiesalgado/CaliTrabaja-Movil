# cambiar_contrasena_view.py
import flet as ft
import re
from app.components.nav import nav_bar
from app.API_services.cambiar_contra_olvidada import cambio_contra_usu
from . import  Inicio

def cambiar_contrasena(page: ft.Page, cambiar_pantalla, token=None):
    page.title = "Cambiar contraseña"
    max_content_width = 600
    campo_bgcolor = "#D9D9D9"

    # --- ESTILOS ---
    label_style = ft.TextStyle(font_family="OswaldBold", size=16, weight=ft.FontWeight.BOLD)

    # --- CAMPOS ---
    nueva_contrasena_field = ft.TextField(
        label="Nueva Contraseña",
        label_style=label_style,
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor=campo_bgcolor,
        expand=True
    )

    repetir_contrasena_field = ft.TextField(
        label="Repetir Contraseña",
        label_style=label_style,
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor=campo_bgcolor,
        expand=True
    )

    message_text = ft.Text("", size=14, color="red", weight=ft.FontWeight.BOLD)

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
        pwd = nueva_contrasena_field.value or ""

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
    nueva_contrasena_field.on_change = validar_password

    # --- ACCIÓN CAMBIAR ---
    def cambiar(e):
        nueva = nueva_contrasena_field.value.strip()
        repetir = repetir_contrasena_field.value.strip()

        if not nueva or not repetir:
            message_text.value = "Por favor, complete ambos campos."
        elif nueva != repetir:
            message_text.value = "Las contraseñas no coinciden."
        elif len(nueva) < 6 or not re.search(r"[A-Z]", nueva):
            message_text.value = "La contraseña no cumple con los requisitos."
        else:
            message_text.value = "✅ Contraseña cambiada exitosamente."
            data={"nueva_contraseña": nueva, "confirmar_contraseña":repetir}
            cambio_contra_usu(token, data)
            Inicio.pantalla_inicio(page, cambiar_pantalla)
        page.update()

    # --- UI ---
    def build_content(page_width):
        container_width = min(page_width * 0.95, max_content_width)
        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # NAV SUPERIOR
                nav_bar(page, page_width, show_back=False),

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
                                    "Elige una nueva contraseña",
                                    size=30,
                                    color="#3EAEB1",
                                    font_family="OswaldBold",
                                    weight=ft.FontWeight.BOLD,
                                    text_align="center"
                                )
                            ),
                            # --- Nueva contraseña ---
                            ft.Container(
                                bgcolor=campo_bgcolor,
                                border_radius=8,
                                padding=ft.padding.only(left=12, right=8, top=5, bottom=5),
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(name="lock", color="#3EAEB1"),
                                        nueva_contrasena_field
                                    ]
                                )
                            ),
                            reglas_columna,
                            # --- Repetir contraseña ---
                            ft.Container(
                                bgcolor=campo_bgcolor,
                                border_radius=8,
                                padding=ft.padding.only(left=12, right=8, top=5, bottom=5),
                                content=ft.Row(
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(name="lock", color="#3EAEB1"),
                                        repetir_contrasena_field
                                    ]
                                )
                            ),
                            message_text,
                            # --- Botón Cambiar ---
                            ft.Container(
                                padding=ft.padding.only(top=1),
                                content=ft.ElevatedButton(
                                    content=ft.Text(
                                        "Cambiar",
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
                                    on_click=cambiar
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


# 🔹 Bloque para ejecutar en emulador Flet
if __name__ == "__main__":
    def main(page: ft.Page):
        def cambiar_pantalla(nombre):
            print(f"Navegar a: {nombre}")

        cambiar_contrasena(page, cambiar_pantalla)

    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
