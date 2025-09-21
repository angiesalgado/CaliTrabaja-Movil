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
        page.go("/chat")

    def reportar(e):
        contacto = e.control.data
        print(f"Abriendo modal de reporte para: {contacto['nombre']}")
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

    # callback menú inferior
    def on_bottom_nav_click(index):
        if callable(cambiar_pantalla):
            if index == 0:
                cambiar_pantalla("inicio")
            elif index == 1:
                cambiar_pantalla("categorias")
            elif index == 2:
                cambiar_pantalla("mensajes")
            elif index == 3:
                cambiar_pantalla("guardados")
            elif index == 4:
                cambiar_pantalla("menu")
        else:
            if index == 0:
                page.go("/")
            elif index == 1:
                page.go("/categorias")
            elif index == 2:
                page.go("/mensajes")
            elif index == 3:
                page.go("/guardados")
            elif index == 4:
                page.go("/menu")

    # callback del botón volver
    def volver_a_inicio_event(e):
        if callable(cambiar_pantalla):
            cambiar_pantalla("inicio")
        else:
            page.go("/")

    return ft.View(
        "/mensajes",
        bgcolor="white",
        padding=0,
        controls=[
            nav_chats(page, volver_callback=volver_a_inicio_event),
            ft.Column(items, expand=True, scroll="auto"),
            ft.Container(
                content=menu_inferior(2, on_bottom_nav_click),
                bgcolor="white",
                padding=5
            )
        ]
    )


# -------------------
# Pantalla: Chat individual (❌ sin menú inferior)
# -------------------
def chat_view(page: ft.Page):
    contacto = page.session.get("contacto") or {"nombre": "Contacto", "foto": None}
    mensajes = ft.Column(expand=True, spacing=10, scroll="auto")

    def enviar_mensaje(e):
        if caja_mensaje.value.strip() != "":
            texto = caja_mensaje.value.strip()
            hora_envio = datetime.now().strftime("%I:%M %p")
            hora_envio = hora_envio.lstrip("0").replace("AM", "a. m.").replace("PM", "p. m.")

            avg_char_px = 20
            padding_for_time_and_inner = 7
            min_bubble = 50
            max_bubble = 250

            estimated_width = len(texto) * avg_char_px + padding_for_time_and_inner
            bubble_width = max(min_bubble, min(max_bubble, int(estimated_width)))
            text_width = max(33, bubble_width - 53)

            mensajes.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Row(
                                spacing=5,
                                vertical_alignment="end",
                                controls=[
                                    ft.Text(
                                        texto,
                                        color="White",
                                        size=14,
                                        no_wrap=False,
                                        max_lines=None,
                                        width=text_width
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            hora_envio,
                                            size=10,
                                            color="White",
                                        ),
                                        margin=ft.margin.only(left=-5),
                                    ),
                                ]
                            ),
                            bgcolor="#3EAEB1",
                            padding=10,
                            border_radius=15,
                            width=bubble_width,
                        )
                    ],
                    alignment="end"
                )
            )

            caja_mensaje.value = ""
            caja_mensaje.update()
            mensajes.update()

    header = ft.SafeArea(
        top=False,
        left=False,
        right=False,
        bottom=False,
        content=ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, icon_size=50, icon_color="#3EAEB1",
                                  on_click=lambda e: page.go("/mensajes")),
                    ft.CircleAvatar(foreground_image_src=contacto.get("foto")),
                    ft.Text(contacto.get("nombre"), size=18, weight="bold", color="#3EAEB1"),
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
