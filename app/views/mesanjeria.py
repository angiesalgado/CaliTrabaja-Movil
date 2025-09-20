import flet as ft
from datetime import datetime, timedelta

# -------------------
# NAV SUPERIOR DE CHATS (gris)
# -------------------
def nav_chats(page: ft.Page, volver_callback=None):
    text_size = 24 if page.width < 400 else 28
    icon_size = 50

    return ft.SafeArea(
        top=False,
        left=False,
        right=False,
        bottom=False,
        content=ft.Container(
            width=float("inf"),
            height=80,
            bgcolor="#F5F5F5",  # fondo gris claro
            padding=ft.padding.only(left=-10, right=0),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_color="#3EAEB1",
                        icon_size=icon_size,
                        on_click=volver_callback
                    ),
                    ft.Text(
                        "Chats",
                        color="#3EAEB1",
                        size=text_size,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(width=icon_size)
                ]
            )
        )
    )

# -------------------
# Función para formatear hora / fecha estilo WhatsApp
# -------------------
def formatear_fecha_hora(fecha: datetime):
    hoy = datetime.now().date()
    if fecha.date() == hoy:
        return fecha.strftime("%H:%M")
    elif fecha.date() == hoy - timedelta(days=1):
        return "Ayer"
    elif fecha.year == hoy.year:
        return fecha.strftime("%d %b")
    else:
        return fecha.strftime("%d/%m/%y")

# -------------------
# Pantalla: Lista de chats
# -------------------
def lista_chats(page: ft.Page):

    def abrir_chat(e):
        contacto = e.control.data
        page.session.set("contacto", contacto)
        page.go("/chat")

    def reportar(e):
        print(f"Reportar chat con: {e.control.data['nombre']}")

    def eliminar(e):
        print(f"Eliminar chat con: {e.control.data['nombre']}")

    chats = [
        {
            "nombre": "Juan Pérez",
            "ultimo": "Nos vemos mañana",
            "foto": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
            "hora": datetime.now() - timedelta(minutes=10),
        },
        {
            "nombre": "María López",
            "ultimo": "Gracias por la info!",
            "foto": "https://cdn-icons-png.flaticon.com/512/194/194938.png",
            "hora": datetime.now() - timedelta(days=1),
        },
        {
            "nombre": "Carlos Ruiz",
            "ultimo": "Te mando el archivo",
            "foto": "https://cdn-icons-png.flaticon.com/512/236/236831.png",
            "hora": datetime.now() - timedelta(days=3),
        },
    ]

    items = []
    for c in chats:
        items.append(
            ft.Container(
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # Avatar + Nombre + Último mensaje
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.CircleAvatar(foreground_image_src=c["foto"]),
                                ft.Column(
                                    spacing=2,
                                    alignment=ft.MainAxisAlignment.START,
                                    controls=[
                                        ft.Text(c["nombre"], weight="bold", color="black", no_wrap=True),
                                        ft.Text(c["ultimo"], size=12, color=ft.Colors.GREY, no_wrap=True),
                                    ]
                                )
                            ]
                        ),
                        # Hora + Menú en fila (hora antes de los puntos)
                        ft.Row(
                            spacing=6,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(formatear_fecha_hora(c["hora"]), size=11, color=ft.Colors.GREY),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_HORIZ,   # tres puntos horizontales
                                    items=[
                                        ft.PopupMenuItem(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.ERROR_OUTLINE, color="#3EAEB1", size=18),
                                                    ft.Text("Reportar", color="black"),
                                                ]
                                            ),
                                            data=c,
                                            on_click=reportar
                                        ),
                                        ft.PopupMenuItem(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.DELETE_OUTLINE, color="#3EAEB1", size=18),
                                                    ft.Text("Eliminar", color="black"),
                                                ]
                                            ),
                                            data=c,
                                            on_click=eliminar
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                ),
                on_click=abrir_chat,
                data=c,
            )
        )

    return ft.View(
        "/",
        bgcolor="white",
        padding=0,
        controls=[
            nav_chats(page, volver_callback=lambda e: print("Ya estás en la lista ")),
            ft.Column(items, expand=True, scroll="auto")
        ]
    )

# -------------------
# Pantalla: Chat individual
# -------------------
def chat_view(page: ft.Page):
    contacto = page.session.get("contacto")

    mensajes = ft.Column(expand=True, spacing=10, scroll="auto")

    def enviar_mensaje(e):
        if caja_mensaje.value.strip() != "":
            hora_envio = datetime.now().strftime("%H:%M")
            mensajes.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(caja_mensaje.value, color="white"),
                                    ft.Text(hora_envio, size=10, color="white", text_align="end"),
                                ],
                                spacing=2,
                                tight=True,
                            ),
                            bgcolor="#3EAEB1",
                            padding=10,
                            border_radius=15,
                            width=220,
                        )
                    ],
                    alignment="end"
                )
            )
            caja_mensaje.value = ""
            mensajes.update()

    header = ft.SafeArea(
        top=False,
        left=False,
        right=False,
        bottom=False,
        content=ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#3EAEB1", on_click=lambda e: page.go("/")),
                    ft.CircleAvatar(foreground_image_src=contacto["foto"]),
                    ft.Text(contacto["nombre"], size=18, weight="bold", color="#3EAEB1"),
                ],
                spacing=10
            ),
            bgcolor="#F5F5F5",
            padding=10,
            margin=0
        )
    )

    caja_mensaje = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        border_radius=30,
        content_padding=10,
        color="black"
    )

    boton_enviar = ft.IconButton(
        icon=ft.Icons.SEND,
        bgcolor="#3EAEB1",
        icon_color="white",
        on_click=enviar_mensaje
    )

    input_box = ft.Container(
        content=ft.Row([caja_mensaje, boton_enviar], spacing=5),
        bgcolor="white",
        padding=5
    )

    return ft.View(
        "/chat",
        bgcolor="white",
        padding=0,
        controls=[
            header,
            ft.Container(content=mensajes, expand=True, padding=10),
            input_box
        ]
    )

# -------------------
# App principal con rutas
# -------------------
def main(page: ft.Page):

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(lista_chats(page))
        elif page.route == "/chat":
            page.views.append(chat_view(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=9000)
