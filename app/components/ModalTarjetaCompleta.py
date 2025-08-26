import flet as ft

class ModalTarjetaCompleta:
    def __init__(self):
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="transparent",   # 🔹 Fondo transparente
            content=ft.Container(),  # Luego insertamos la tarjeta
            actions=[]               # Sin botones por defecto
        )

    def set_content(self, nombre, profesion, descripcion, costo, calificacion):
        # ⭐ Estrellas
        stars = ft.Row(
            [ft.Icon(
                ft.Icons.STAR if i < calificacion else ft.Icons.STAR_BORDER,
                color="#3EAEB1",
                size=16
            ) for i in range(5)],
            spacing=2,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Botón "X" arriba a la derecha
        cerrar_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=20,
            icon_color="black",
            on_click=self.cerrar,
            style=ft.ButtonStyle(padding=0),
        )

        # 📌 Tarjeta ajustada en altura
        tarjeta_completa = ft.Container(
            width=280,
            height=400,  # 🔹 Mantienes la altura controlada
            padding=16,
            bgcolor="white",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Row([ft.Container(expand=1), cerrar_btn]),

                    ft.CircleAvatar(radius=35, bgcolor=ft.Colors.GREY_300),
                    ft.Text(f"COP {costo}/h", size=12, color="black"),
                    ft.Text(nombre, weight=ft.FontWeight.BOLD, size=18, text_align=ft.TextAlign.CENTER),
                    stars,
                    ft.Text(profesion, size=14, color="black54", text_align=ft.TextAlign.CENTER),

                    ft.Text("Descripción", weight=ft.FontWeight.BOLD, size=13),
                    ft.Container(
                        content=ft.Text(descripcion, size=12, text_align=ft.TextAlign.JUSTIFY),
                        # ❌ OJO: quitamos expand=True
                    )
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.START,  # 🔹 Todo arriba
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        # ✅ Insertamos directamente la tarjeta en el modal
        self.dialog.content = tarjeta_completa

    def cerrar(self, e):
        self.dialog.open = False
        e.page.update()
