import flet as ft


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


class ModalReporte:
    def __init__(self, on_guardar=None, on_cancelar=None):
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
            border_radius=15,

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
            modal=False,
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
        # Validar que haya descripción
        if not self.descripcion.value or self.descripcion.value.strip() == "":
            mostrar_snackbar(e.page, "Por favor, añade una descripción del problema", exito=False)
            return

        try:
            # Si hay callback personalizado, lo ejecutamos
            if self.on_guardar:
                resultado = self.on_guardar(self.descripcion.value)

                # Verificar si el resultado indica éxito
                if isinstance(resultado, dict) and resultado.get("success", False):
                    mostrar_snackbar(e.page, "Reporte enviado exitosamente", exito=True)
                    self.dialog.open = False
                    e.page.update()
                elif isinstance(resultado, dict) and not resultado.get("success", True):
                    mostrar_snackbar(e.page, resultado.get("message", "Error al enviar el reporte"), exito=False)
                else:
                    # Si no hay estructura de respuesta clara, asumimos éxito
                    mostrar_snackbar(e.page, "Reporte enviado exitosamente", exito=True)
                    self.dialog.open = False
                    e.page.update()
            else:
                # Si no hay callback, solo cerramos el modal
                mostrar_snackbar(e.page, "Reporte guardado", exito=True)
                self.dialog.open = False
                e.page.update()

        except Exception as ex:
            mostrar_snackbar(e.page, f"Error al enviar reporte: {str(ex)}", exito=False)

    def cancelar(self, e):
        if self.on_cancelar:
            self.on_cancelar()
        self.dialog.open = False
        e.page.update()

    def show(self, page):
        self.descripcion.value = ""
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()