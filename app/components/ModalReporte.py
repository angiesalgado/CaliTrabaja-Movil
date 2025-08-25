import flet as ft

class ModalReporte:
    def __init__(self, on_guardar=None, on_cancelar=None):
        self.on_guardar = on_guardar
        self.on_cancelar = on_cancelar

        # 📝 Campo de texto estilizado
        self.descripcion = ft.TextField(
            multiline=True,
            hint_text="Añade una descripción del problema",
            height=60,

            # 🔹 Estilos visuales
            border="none",  # Sin bordes
            filled=True,
            fill_color="#D9D9D9",  # Fondo gris
            border_radius=10,

            # 🔹 Estilo del texto escrito por el usuario
            text_style=ft.TextStyle(
                font_family="Oswald",
                size=14,
                color=ft.Colors.BLACK
            ),

            # 🔹 Estilo del placeholder
            hint_style=ft.TextStyle(
                font_family="Oswald",
                size=14,
                weight=ft.FontWeight.W_500,  # Medium
                color="#808080",
            ),
        # 🔹 Para que arranque grande y pueda crecer
        min_lines = 4,  # tamaño inicial (como 4 renglones)
        max_lines = None,  # que crezca indefinidamente
        )

        # 📦 Diálogo principal
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#FFFFFF",  # 🔹 Fondo blanco del modal
            content=ft.Container(
                width=380,
                padding=20,
                bgcolor="#FFFFFF",
                border_radius=20,
                content=ft.Column(
                    [
                        ft.Text(
                            "Añadir reporte",
                            size=24,
                            weight="bold",
                            text_align="center",
                            color="#3EAEB1",
                            font_family="Oswald"
                        ),
                        self.descripcion,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Guardar",
                                    bgcolor="#3EAEB1",
                                    color=ft.Colors.WHITE,
                                    on_click=self.guardar,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                                        # 🔹 Más ancho, menos alto
                                    )
                                ),
                                ft.OutlinedButton(
                                    "Cancelar",
                                    on_click=self.cancelar,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                                        # 🔹 Igual tamaño que Guardar
                                        side=ft.BorderSide(1, "#000000"),  # 🔹 Borde negro
                                        color="#000000"
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        )
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=35  # 🔹 separación uniforme entre título, campo y botones
                )
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def guardar(self, e):
        if self.on_guardar:
            self.on_guardar(self.descripcion.value)
        self.dialog.open = False
        e.page.update()

    def cancelar(self, e):
        if self.on_cancelar:
            self.on_cancelar()
        self.dialog.open = False
        e.page.update()

    def show(self, page):
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()
