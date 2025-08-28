import flet as ft

class ModalReporte:
    def __init__(self, on_guardar=None, on_cancelar=None, alto_texto=150):
        self.on_guardar = on_guardar
        self.on_cancelar = on_cancelar

        # 🔹 TextField dentro de un Container para fijar altura
        self.descripcion = ft.TextField(
            multiline=True,
            min_lines=6,
            max_lines=6,
            hint_text="Añade una descripción del problema",
            border="none",
            filled=True,
            fill_color="#D9D9D9",
            border_radius=10,

            # 🔹 Estilo del texto escrito
            text_style=ft.TextStyle(
                font_family="Oswald",
                size=14,
                color=ft.Colors.BLACK
            ),

            # 🔹 Estilo del placeholder
            hint_style=ft.TextStyle(
                font_family="Oswald",
                size=14,
                weight=ft.FontWeight.W_500,
                color="#808080",
            ),

        )


        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#FFFFFF",
            content=ft.Container(
                width=380,
                height=260,

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
                                    width=110,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                    )
                                ),
                                ft.OutlinedButton(
                                    "Cancelar",
                                    on_click=self.cancelar,
                                    width=110,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        bgcolor="#F2F2F2",
                                        color="black",
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15
                        )
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def guardar(self, e):
        if self.on_guardar:

            self.on_guardar(self.descripcion.content.value)
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
