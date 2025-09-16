# components/ModalAcceso.py
import flet as ft

def mostrar_modal_acceso(page, cambiar_pantalla):
    """Muestra modal cuando intentan acceder sin estar logueados"""

    def cerrar_modal(e=None):
        modal.open = False
        page.update()

    def ir_ingresar(e):
        cerrar_modal()
        cambiar_pantalla("login")

    def ir_registro(e):
        cerrar_modal()
        cambiar_pantalla("registro")

    # Botón ingresar (color #3EAEB1)
    btn_ingresar = ft.ElevatedButton(
        "Ingresar",
        bgcolor="#3EAEB1",
        color=ft.Colors.WHITE,
        width=220,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            overlay_color={"": "#2F8F91"},
            text_style={"": ft.TextStyle(
                font_family="Oswald",
                size=16,
                weight=ft.FontWeight.W_600,
                color="white"
            )}
        ),
        on_click=ir_ingresar,
    )

    # Botón crear cuenta (blanco con borde negro)
    btn_crear = ft.OutlinedButton(
        "Crear cuenta",
        width=220,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor="#f8f8f8",
            color="black",
            side=ft.BorderSide(1, "#E5E5E5"),
            text_style={"": ft.TextStyle(
                font_family="Oswald",
                size=16,
                weight=ft.FontWeight.W_600,
                color="black"
            )}
        ),
        on_click=ir_registro,
    )

    # Contenedor con X flotante
    modal_content = ft.Stack(
        [
            ft.Container(
                width=320,
                bgcolor="#FFFFFF",
                border_radius=20,
                padding=ft.padding.all(16),
                content=ft.Column(
                    [
                        ft.Text(
                            "Debes iniciar sesión o registrarte\npara acceder a esta sección",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            text_align="center",
                            color="black",
                            font_family="Oswald"
                        ),
                        btn_ingresar,
                        btn_crear
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12
                ),
            ),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_size=20,
                tooltip="Cerrar",
                on_click=cerrar_modal,
                right=-10,
                top=-10,
            ),
        ]
    )

    modal = ft.AlertDialog(
        modal=False,  # 👈 se puede cerrar clickeando fuera
        bgcolor="#FFFFFF",
        content=modal_content,
    )

    if modal not in page.overlay:
        page.overlay.append(modal)

    modal.open = True
    page.update()
