import flet as ft

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
            padding=ft.padding.only(left=-10, right=0),  # quita margen izquierdo
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_color="#3EAEB1",   # color corporativo
                        icon_size=icon_size,
                        on_click=volver_callback
                    ),
                    ft.Text(
                        "Chats",
                        color="#3EAEB1",
                        size=text_size,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(width=icon_size)  # espacio derecho vacío
                ]
            )
        )
    )

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
        {"nombre": "Juan Pérez", "ultimo": "Nos vemos mañana", "foto": "https://cdn-icons-png.flaticon.com/512/149/149071.png"},
        {"nombre": "María López", "ultimo": "Gracias por la info!", "foto": "https://cdn-icons-png.flaticon.com/512/194/194938.png"},
        {"nombre": "Carlos Ruiz", "ultimo": "Te mando el archivo", "foto": "https://cdn-icons-png.flaticon.com/512/236/236831.png"},
    ]

    items = []
    for c in chats:
        items.append(
            ft.ListTile(
                leading=ft.CircleAvatar(foreground_image_src=c["foto"]),
                title=ft.Text(c["nombre"], weight="bold"),
                subtitle=ft.Text(c["ultimo"], size=12, color=ft.Colors.GREY),
                on_click=abrir_chat,
                data=c,
                trailing=ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT,
                    items=[
                        ft.PopupMenuItem(
                            text="Reportar",
                            icon=ft.Icons.ERROR_OUTLINE,
                            data=c,
                            on_click=reportar
                        ),
                        ft.PopupMenuItem(
                            text="Eliminar",
                            icon=ft.Icons.DELETE,
                            data=c,
                            on_click=eliminar
                        ),
                    ]
                )
            )
        )

    return ft.View(
        "/",
        bgcolor="white",  # fondo blanco en la lista
        padding=0,
        controls=[
            nav_chats(page, volver_callback=lambda e: print("Ya estás en la lista 👀")),
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
            mensajes.controls.append(
                ft.Row(
                    [ft.Container(ft.Text(caja_mensaje.value, color="white"),
                                  bgcolor="#3EAEB1",
                                  padding=10,
                                  border_radius=15,
                                  width=200)],
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
            bgcolor="#F5F5F5",  # estilo WhatsApp
            padding=10,
            margin=0
        )
    )

    caja_mensaje = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        border_radius=30,
        content_padding=10,
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
        bgcolor="white",  # fondo blanco en chat
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
