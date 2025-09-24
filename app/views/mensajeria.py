import flet as ft
from datetime import datetime, timedelta
from app.components.ModalReporte import ModalReporte
from app.components.menu_inferior import menu_inferior   # ✅ import del menú


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
            bgcolor="#F5F5F5",
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
def lista_chats(page: ft.Page, cambiar_pantalla=None):

    modal_reporte = ModalReporte(
        on_guardar=lambda desc: print(f"Reporte guardado: {desc}"),
        on_cancelar=lambda: print("Reporte cancelado")
    )
    if modal_reporte.dialog not in page.overlay:
        page.overlay.append(modal_reporte.dialog)

    def abrir_chat(e):
        contacto = e.control.data
        page.session.set("contacto", contacto)
        if callable(cambiar_pantalla):
            cambiar_pantalla("chat")

    def reportar(e):
        contacto = e.control.data
        page.dialog = modal_reporte.dialog
        modal_reporte.dialog.open = True
        page.update()

    def eliminar(e):
        contacto = e.control.data
        print(f"Eliminar chat con: {contacto['nombre']}")

    # Ejemplo de datos
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
                        ft.Row(
                            spacing=6,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(formatear_fecha_hora(c["hora"]), size=11, color=ft.Colors.GREY),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_HORIZ,
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
                                            on_click=lambda e: mostrar_modal_eliminar_mensaje(page, mensaje_id="123"),
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

    # callback menú inferior
    def on_bottom_nav_click(index):
        if index == 0:  # Inicio
            cambiar_pantalla("inicio")
        elif index == 1:  # Categorias
            cambiar_pantalla("categorias")
        elif index == 2:  # Mensajes
            cambiar_pantalla("mensajes")
        elif index == 3:  # Guardados
            cambiar_pantalla("guardados")
        elif index == 4:  # Menú
            cambiar_pantalla("menu")

    # callback del botón volver
    def volver_a_inicio_event(e):
        if callable(cambiar_pantalla):
            cambiar_pantalla("inicio")

    # layout principal
    layout = ft.Column(
        controls=[
            nav_chats(page, volver_callback=volver_a_inicio_event),
            ft.Column(items, expand=True, scroll="auto"),
        ],
        expand=True
    )

    # menú inferior fijo
    page.bottom_appbar = ft.BottomAppBar(
        content=menu_inferior(2, on_bottom_nav_click),
        bgcolor=ft.Colors.WHITE,
        elevation=0,
    )

    return layout


# -------------------
# Pantalla: Chat individual
# -------------------
def chat_view(page: ft.Page, cambiar_pantalla=None):
    contacto = page.session.get("contacto") or {"nombre": "Contacto", "foto": None}
    mensajes = ft.Column(expand=True, spacing=10, scroll="auto")

    def enviar_mensaje(e):
        if caja_mensaje.value and caja_mensaje.value.strip() != "":
            texto = caja_mensaje.value.strip()
            hora_envio = datetime.now().strftime("%I:%M %p").lstrip("0").replace("AM", "a. m.").replace("PM", "p. m.")

            try:
                max_bubble_width = int(page.width * 0.65)
            except Exception:
                max_bubble_width = 320
            if max_bubble_width < 220:
                max_bubble_width = 220

            bubble = ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    texto,
                                    color="White",
                                    size=14,
                                    no_wrap=False,
                                    max_lines=None,
                                    width=max_bubble_width,
                                ),
                                ft.Text(
                                    hora_envio,
                                    size=10,
                                    color="White",
                                ),
                            ],
                            spacing=6,
                            horizontal_alignment=ft.CrossAxisAlignment.END
                        ),
                        bgcolor="#3EAEB1",
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        border_radius=15,
                        width=max_bubble_width + 30
                    )
                ],
                alignment="end"
            )

            mensajes.controls.append(bubble)
            caja_mensaje.value = ""
            caja_mensaje.update()
            mensajes.update()

            try:
                mensajes.controls[-1].scroll_into_view()
            except Exception:
                pass

    # función para volver
    def volver(e):
        page.bottom_appbar = None
        if callable(cambiar_pantalla):
            cambiar_pantalla("mensajes")
        page.update()

    # Header
    header = ft.SafeArea(
        top=False,
        left=False,
        right=False,
        bottom=False,
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_size=40,
                        icon_color="#3EAEB1",
                        on_click=volver
                    ),
                    ft.CircleAvatar(foreground_image_src=contacto.get("foto")),
                    ft.Text(
                        contacto.get("nombre"),
                        size=18,
                        weight="bold",
                        color="#3EAEB1"
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#F5F5F5",
            padding=ft.padding.only(left=5, right=10),
        )
    )

    caja_mensaje = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        border_radius=30,
        content_padding=10,
        color="black",
        multiline=True,
        min_lines=1,
        max_lines=3,
        focused_border_color="#3EAEB1"
    )

    boton_enviar = ft.IconButton(
        icon=ft.Icons.SEND,
        bgcolor="#3EAEB1",
        icon_color="white",
        on_click=enviar_mensaje
    )

    bottom_content = ft.SafeArea(
        bottom=True,
        content=ft.Container(
            content=ft.Row(
                controls=[caja_mensaje, boton_enviar],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="white",
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            width=float("inf"),
        )
    )

    page.bottom_appbar = ft.BottomAppBar(
        content=bottom_content,
        bgcolor="white",
        elevation=6
    )

    mensajes_container = ft.Container(
        content=mensajes,
        expand=True,
        padding=ft.padding.only(top=10, left=10, right=10, bottom=10)
    )

    return ft.Column(
        controls=[
            header,
            mensajes_container
        ],
        expand=True
    )


def mostrar_modal_eliminar_mensaje(page, mensaje_id=None):
    def confirmar_eliminar(e):
        print(f"Mensaje {mensaje_id} eliminado (simulación frontend).")
        modal.open = False
        page.update()

    def cancelar(e):
        modal.open = False
        page.update()

    btn_aceptar = ft.ElevatedButton(
        "Aceptar",
        bgcolor="#3EAEB1",
        color=ft.Colors.WHITE,
        width=110,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20)
        ),
        on_click=confirmar_eliminar,
    )

    btn_cancelar = ft.OutlinedButton(
        "Cancelar",
        width=110,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20)
        ),
        on_click=cancelar,
    )

    modal = ft.AlertDialog(
        modal=False,
        bgcolor="#FFFFFF",
        content=ft.Container(
            width=320,
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Text(
                        "¿Deseas eliminar este mensaje?",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align="center",
                        color="#666666",
                        font_family="Oswald"
                    ),
                    ft.Row(
                        [btn_aceptar, btn_cancelar],
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

    if modal not in page.overlay:
        page.overlay.append(modal)

    modal.open = True
    page.update()
