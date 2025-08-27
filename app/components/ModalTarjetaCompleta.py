import flet as ft

class ModalTarjetaCompleta:
    def __init__(self):
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="transparent",   # 🔹 Fondo transparente
            content=ft.Container(),  # Luego insertamos la tarjeta
            actions=[]
        )

    def set_content(self, nombre, profesion, descripcion, costo, calificacion, page: ft.Page = None):
        # ⭐ Estrellas
        stars = ft.Row(
            [
                ft.Icon(
                    ft.Icons.STAR if i < calificacion else ft.Icons.STAR_BORDER,
                    color="#3EAEB1",
                    size=16
                ) for i in range(5)
            ],
            spacing=2,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Botón "X"
        cerrar_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=20,
            icon_color="black",
            on_click=self.cerrar,
            style=ft.ButtonStyle(padding=0),
        )

        # 🔹 Detectar si es pantalla pequeña (ej: celular)
        es_pantalla_pequena = page and page.width < 480

        # 📌 Tarjeta en sí
        tarjeta_completa = ft.Container(
            width=380 if not es_pantalla_pequena else  ft.infinity,   # 🔹 más ancha en celular
            height=380 if not es_pantalla_pequena else 320,
            padding=ft.padding.only(top=3, left=15, right=15, bottom=10),  # 🔹 ajusta el espacio interno
            bgcolor="white",
            border_radius=20,
            content=ft.Column(
                [
                    # Fila con botón cerrar
                    ft.Row([ft.Container(expand=1), cerrar_btn]),

                    ft.CircleAvatar(
                        radius=36 if es_pantalla_pequena else 38,
                        bgcolor=ft.Colors.GREY_300
                    ),
                    ft.Text(
                        f"COP {costo}/h",
                        size=12 if es_pantalla_pequena else 13,
                        color="black"
                    ),
                    ft.Text(
                        nombre,
                        weight=ft.FontWeight.BOLD,
                        size=18 if es_pantalla_pequena else 20,
                        text_align=ft.TextAlign.CENTER
                    ),
                    stars,
                    ft.Text(
                        profesion,
                        size=13 if es_pantalla_pequena else 15,
                        color="black54",
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Divider(
                        height=6 if es_pantalla_pequena else 8,
                        color="transparent"
                    ),

                    ft.Text(
                        "Descripción",
                        weight=ft.FontWeight.BOLD,
                        size=13 if es_pantalla_pequena else 14
                    ),
                    ft.Container(
                        content=ft.Text(
                            descripcion,
                            size=12 if es_pantalla_pequena else 13,
                            text_align=ft.TextAlign.JUSTIFY
                        ),
                        padding=ft.padding.only(
                            left=6 if es_pantalla_pequena else 8,
                            right=6 if es_pantalla_pequena else 8
                        )
                    )
                ],
                spacing=6 if es_pantalla_pequena else 8,
                alignment=ft.MainAxisAlignment.START,   # 🔹 contenido pegado arriba dentro de la tarjeta
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True
            )
        )

        # 📌 Contenedor con espaciador arriba para subir la tarjeta
        self.dialog.content = ft.Column(
            [
                ft.Container(height=20 if es_pantalla_pequena else 80),  # 👈 controla cuánto sube
                tarjeta_completa
            ],
            alignment=ft.MainAxisAlignment.START,   # 🔹 que todo se quede arriba
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def cerrar(self, e):
        self.dialog.open = False
        e.page.update()
