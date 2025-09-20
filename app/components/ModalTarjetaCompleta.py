import flet as ft

class ModalTarjetaCompleta:
    def __init__(self):   # ✅ doble underscore
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="transparent",
            content=ft.Container(),
            actions=[]
        )

    def set_content(self, foto_perfil, nombre, profesion, descripcion, costo, calificacion, page: ft.Page = None):

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

        es_pantalla_pequena = page and page.width < 480

        base_url = "http://localhost:5000/static/uploads/perfiles/"

        if foto_perfil and foto_perfil.lower() != "none":
            img_url = f"{base_url}{foto_perfil}"
        else:
            img_url = f"{base_url}defecto.png"  # imagen por defecto

        print(f"RUTA IMAGEN {img_url}")

        tarjeta_completa = ft.Container(
            width=380 if not es_pantalla_pequena else ft.infinity,
            padding=ft.padding.only(top=5, left=15, right=15, bottom=10),
            bgcolor="white",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(expand=1),
                            cerrar_btn
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.CircleAvatar(
                        foreground_image_src=img_url,
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
                    ft.Divider(height=6, color="transparent"),
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
                        padding=ft.padding.only(left=8, right=8)
                    )
                ],
                spacing=2,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True
            )
        )

        # 🔹 Centramos el modal
        self.dialog.content = ft.Container(
            expand=True,
            content=tarjeta_completa,
            alignment=ft.alignment.center
        )

    def cerrar(self, e):
        self.dialog.open = False
        e.page.update()
