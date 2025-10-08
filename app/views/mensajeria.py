import flet as ft
from datetime import datetime, timedelta
from app.components.ModalReporte import ModalReporte
from app.components.menu_inferior import menu_inferior  # ✅ import del menú
from app.socket_cliente import sio
import requests

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
def formatear_fecha_hora(fecha_str):
    if not fecha_str:
        return ""
    try:
        fecha = datetime.fromisoformat(fecha_str)
    except Exception:
        return fecha_str
    return fecha.strftime("%d/%m/%Y %H:%M")

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

    def abrir_chat(e, otro_usuario_id):
        contacto = e.control.data
        page.session.set("contacto", contacto)
        if callable(cambiar_pantalla):
            cambiar_pantalla("chat", receptor_id=otro_usuario_id)

    def reportar(e):
        contacto = e.control.data
        page.dialog = modal_reporte.dialog
        modal_reporte.dialog.open = True
        page.update()

    # 🔥 Aquí pedimos los chats reales al backend
    token = getattr(page, "session_token", None)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get("http://127.0.0.1:5000/api/chats", headers=headers)
    print("TEXT:", resp.text)

    data = resp.json()

    chats = data.get("chats", [])  # <- tu backend debe devolver [{"usuario_id":..,"nombre":..,"ultimo":..,"foto":..,"hora":..}, ...]

    items = []
    for c in chats:
        receptor_id = c["usuario_id"]
        nombre = c.get("nombre", "")
        ultimo = c.get("ultimo_texto", "")
        hora = formatear_fecha_hora(c.get("hora"))

        img_src = c.get("foto") or "https://via.placeholder.com/150"

        items.append(
            ft.GestureDetector(
                on_tap=lambda e, receptor_id=receptor_id: cambiar_pantalla("chat", receptor_id=receptor_id),
                content=ft.Container(
                    padding=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.CircleAvatar(foreground_image_src=img_src),
                                    ft.Column(
                                        spacing=2,
                                        alignment=ft.MainAxisAlignment.START,
                                        controls=[
                                            ft.Text(nombre, weight="bold", color=ft.Colors.BLACK, no_wrap=True),
                                            ft.Text(ultimo, size=12, color=ft.Colors.GREY, no_wrap=True),
                                        ]
                                    )
                                ]
                            ),
                            ft.Text(hora, size=11, color=ft.Colors.GREY),
                        ]
                    )
                )
            )
        )

    # callback menú inferior
    def on_bottom_nav_click(index):
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

    def volver_a_inicio_event(e):
        if callable(cambiar_pantalla):
            cambiar_pantalla("inicio")

    layout = ft.Column(
        controls=[
            nav_chats(page, volver_callback=volver_a_inicio_event),
            ft.Column(items, expand=True, scroll="auto"),
        ],
        expand=True
    )

    page.bottom_appbar = ft.BottomAppBar(
        content=menu_inferior(2, on_bottom_nav_click),
        bgcolor=ft.Colors.WHITE,
        elevation=0,
    )

    return layout


# -------------------
# Pantalla: Chat individual (con Socket.IO)
# -------------------
def chat_view(page: ft.Page, cambiar_pantalla, receptor_id: int):
    mensajes_lista = []

    mensajes_column = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True
    )
    mensajes_lista = []
    input_field = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        border=ft.InputBorder.OUTLINE,
    )

    user_id = page.session.get("user_id")

    if not sio.connected:
        sio.connect("http://127.0.0.1:5000")
        sio.emit("identify", {"user_id": user_id})
        sio.emit("join_chat", {"user_id": user_id, "other_user_id": receptor_id})

    def volver(e):
        if sio.connected:
            sio.emit("leave_chat", {
                "user_id": user_id,
                "other_user_id": receptor_id
            })
            sio.disconnect()  # <-- muy importante para permitir volver a conectar luego
        if callable(cambiar_pantalla):
            cambiar_pantalla("mensajes")

    def agregar_burbuja(texto, emisor, mensajes, fecha, leido=False):
        es_mio = emisor == user_id

        burbuja = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(texto, size=14),
                    padding=10,
                    bgcolor=ft.Colors.BLUE_100 if es_mio else ft.Colors.GREY_200,
                    border_radius=10,
                    margin=10,
                    width=300
                )
            ],
            alignment=ft.MainAxisAlignment.END if es_mio else ft.MainAxisAlignment.START
        )

        mensajes_lista.append(burbuja)

    def recibir_historial(data):
        print("✅ Handler 'chat_history' activado")
        print("📦 Historial recibido:", data)

        mensajes_lista.clear()

        for m in data:
            agregar_burbuja(
                texto=m.get("texto"),
                emisor=m.get("emisor"),
                mensajes=mensajes_column,
                fecha=m.get("fecha"),
                leido=m.get("leido", False)
            )

        mensajes_column.controls = mensajes_lista
        print("📊 Cantidad de burbujas generadas:", len(mensajes_lista))
        page.update()

        sio.emit("leer_mensajes", {
            "user_id": user_id,
            "other_user_id": receptor_id
        })
        page.update()
        sio.emit("leer_mensajes", {
            "user_id": user_id,
            "other_user_id": receptor_id
        })

    # Registrar si no existe aún
    if not sio.handlers.get("chat_history"):
        print("🧠 Registrando handler 'chat_history'")
        sio.on("chat_history", recibir_historial)

        # Marcar mensajes como leídos en el servidor
        if receptor_id:
            sio.emit("leer_mensajes", {
                "user_id": user_id,
                "other_user_id": receptor_id
            })

    def recibir_mensaje(data):
        ...

    if not sio.handlers.get("new_message"):
        sio.on("new_message", recibir_mensaje)

    def mensaje_visto(data):
        ...

    if not sio.handlers.get("mensaje_leido"):
        sio.on("mensaje_leido", mensaje_visto)

    def enviar_mensaje(e):
        texto = input_field.value.strip()
        if not texto:
            return
        sio.emit("send_message", {
            "user_id": user_id,
            "other_user_id": receptor_id,
            "texto": texto
        })
        input_field.value = ""
        input_field.update()

    enviar_btn = ft.IconButton(icon=ft.Icons.SEND, on_click=enviar_mensaje)

    header = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=volver, icon_color="#3EAEB1"),
                ft.Text("Chat", size=18, weight="bold"),
                ft.Container(width=40)
            ]
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        bgcolor="white",
        height=50
    )

    mensajes_lista.append(ft.Text("Mensaje de prueba"))
    mensajes_column.controls = mensajes_lista

    return ft.Column(
        controls=[
            header,  # 🔝 Barra superior fija

            ft.Container(  # 🧭 Área scrollable
                expand=True,
                content=mensajes_column
            ),

            ft.Divider(),  # Línea separadora

            ft.Row(  # 🔽 Barra inferior fija
                controls=[input_field, enviar_btn],
                alignment=ft.MainAxisAlignment.END
            )
        ],
        expand=True
    )


# -------------------
# Modal eliminar mensaje
# -------------------
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
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        on_click=confirmar_eliminar,
    )

    btn_cancelar = ft.OutlinedButton(
        "Cancelar",
        width=110,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
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
                    ft.Text("¿Deseas eliminar este mensaje?",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            text_align="center",
                            color="#666666",
                            font_family="Oswald"),
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

    # -------------------
    # Helper para burbujas de chat
    # -------------------


def agregar_burbuja(texto, es_mio, mensajes, page):
    hora_envio = datetime.now().strftime("%H:%M")
    bubble = ft.Row(
        [
            ft.Container(
                content=ft.Column([
                    ft.Text(texto, color="white", size=14),
                    ft.Text(hora_envio, size=10, color="white"),
                ]),
                bgcolor="#3EAEB1" if es_mio else "#999999",
                padding=10,
                border_radius=15,
            )
        ],
        alignment="end" if es_mio else "start"
    )
    mensajes.controls.append(bubble)
    mensajes.update()
    try:
        mensajes.controls[-1].scroll_into_view()
    except:
        pass