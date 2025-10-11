import flet as ft
from datetime import datetime, timedelta
from app.components.ModalReporte import ModalReporte
from app.components.menu_inferior import menu_inferior  # ✅ import del menú
from app.socket_cliente import sio
import requests
import time
from app.API_services.guardar_calificacion import enviar_calificacion
from app.API_services.guardar_reporte import enviar_reporte

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
def lista_chats(page: ft.Page, cambiar_pantalla, sio, user_id_global):
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
        reportado_id = contacto.get("usuario_id")

        token = obtener_token(page)

        def guardar_reporte(descripcion):
            datos = {
                "descripcion": descripcion,
                "reportado_id": reportado_id
            }

            if not token:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Inicia sesión para enviar un reporte."),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return

            respuesta = enviar_reporte(token, datos)

            if respuesta.get("success"):
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(" Reporte enviado correctamente."),
                    bgcolor="#3EAEB1"
                )
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f" {respuesta.get('message', 'Error al enviar reporte.')}"),
                    bgcolor="red"
                )
            page.snack_bar.open = True
            page.update()

        # Conectamos la función al modal y lo abrimos
        modal_reporte.on_guardar = guardar_reporte
        modal_reporte.show(page)



    # Aquí pedimos los chats reales al backend
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

        # 🔹 Popup menu (Calificar - Reportar - Eliminar)
        popup_menu = ft.PopupMenuButton(
            icon=ft.Icons.MORE_HORIZ,
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.STAR_RATE_OUTLINED, color="#3EAEB1", size=18),
                            ft.Text("Calificar", color="black"),
                        ]
                    ),
                    on_click=lambda e, rid=receptor_id: mostrar_modal_calificar(page, receptor_id=rid),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ERROR_OUTLINE, color="#3EAEB1", size=18),
                            ft.Text("Reportar", color="black"),
                        ]
                    ),
                    data=c,
                    on_click=reportar,
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.DELETE_OUTLINE, color="#3EAEB1", size=18),
                            ft.Text("Eliminar", color="black"),
                        ]
                    ),
                    data=c,
                    on_click=lambda e: mostrar_modal_eliminar_mensaje(page, mensaje_id=c.get("id", "123")),
                ),
            ],
        )

        # 🔹 Card del chat
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
                                    ),
                                ]
                            ),
                            ft.Row(
                                spacing=6,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(hora, size=11, color=ft.Colors.GREY),
                                    popup_menu  # ⬅️ Menú añadido
                                ],
                            ),
                        ],
                    ),
                ),
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
mensajes_map = {}


def chat_view(page: ft.Page, cambiar_pantalla, sio, user_id_global, receptor_id, receptor_nombre):
    # --- 1. DEFINICIÓN DE CONTROLES Y VARIABLES ---

    mensajes_column = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True
    )
    mensajes_lista = []
    mensajes_map = {}  # Almacena {mensaje_id: ft.Icon} para actualización

    input_field = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        border=ft.InputBorder.OUTLINE,
    )

    #user_id = page.session.get("user_id")
    user_id = user_id_global
    try:
        user_id = int(user_id_global)
    except (ValueError, TypeError):
        # Si falla, usamos la versión original, aunque es riesgoso
        user_id = user_id_global

    # --- 2. CONEXIÓN INICIAL Y UNIÓN AL CHAT ---
    if sio.connected:
        # Re-identificamos y nos unimos a la sala (Esto es necesario al re-entrar)
        sio.emit("identify", {"user_id": user_id})
        sio.emit("join_chat", {"user_id": user_id, "other_user_id": receptor_id})

    # ----------------------------------------------------------------------
    # --- 3. FUNCIONES AUXILIARES (Definidas primero para evitar NameError) ---
    # ----------------------------------------------------------------------

    def volver(e):
        # 1. Quitar handlers (ESENCIAL para la re-entrada)
        if sio.handlers.get("chat_history"): sio.off("chat_history")
        if sio.handlers.get("new_message"): sio.off("new_message")
        if sio.handlers.get("message_read"): sio.off("message_read")

        # 2. Salir de la sala (NO DESCONECTAR EL SOCKET GLOBAL)
        if sio.connected:
            sio.emit("leave_chat", {
                "user_id": user_id,
                "other_user_id": receptor_id
            })

        # 3. Limpiar variables y controles
        mensajes_column.controls.clear()
        mensajes_lista.clear()
        mensajes_map.clear()

        # 4. Cambiar de pantalla
        if callable(cambiar_pantalla):
            cambiar_pantalla("mensajes")

    def EstadoMensaje(leido: bool):
        icon_name = ft.Icons.DONE_ALL if leido else ft.Icons.ACCESS_TIME
        icon_color = ft.Colors.LIGHT_BLUE_500 if leido else ft.Colors.GREY_500
        return ft.Icon(name=icon_name, color=icon_color, size=16)

    def agregar_burbuja(texto, emisor, mensajes, fecha, usuario_logueado_id, leido=False, mensaje_id=None):

        # 1. CONVERSIÓN DE TIPO SEGURA
        es_mio = False
        try:
            # Forzamos que ambas IDs sean números enteros para una comparación precisa
            emisor_id_int = int(emisor) if emisor is not None else -1
            usuario_id_int = int(usuario_logueado_id) if usuario_logueado_id is not None else -2

            es_mio = emisor_id_int == usuario_id_int
            print(f"DEBUG BUBBLE: Emisor={emisor_id_int} | Logueado={usuario_id_int} | Texto='{texto[:15]}...' | Resultado={es_mio}")
        except (ValueError, TypeError):
            # Si alguna ID no puede convertirse (ej: 'None' o un texto), es_mio será False.
            es_mio = False
            print(f"DEBUG BUBBLE: Error de conversión. Texto='{texto[:15]}...'")
            # 2. Creamos el control de estado de lectura (solo si el mensaje es nuestro)
        estado_icon = None
        if es_mio:
            estado_icon = EstadoMensaje(leido)

        # 3. El contenido de la burbuja (ft.Column)
        burbuja_content = ft.Column(
            controls=[
                ft.Text(texto, size=14, color=ft.Colors.BLACK),
                ft.Row(
                    controls=[
                        ft.Text(fecha, size=10, color=ft.Colors.BLACK54),
                        estado_icon if es_mio else ft.Container(width=0)
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=5
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=2
        )

        # 4. Contenedor principal de la burbuja
        burbuja_container = ft.Container(
            content=burbuja_content,
            padding=10,
            # ⬅️ Usa es_mio para el color
            bgcolor=ft.Colors.BLUE_100 if es_mio else ft.Colors.GREY_200,
            border_radius=10,
            margin=ft.margin.only(bottom=5),
            width=300
        )

        # 5. Envolvemos en un Row para alinear toda la burbuja
        burbuja = ft.Row(
            controls=[burbuja_container],
            # ⬅️ Usa es_mio para la alineación
            alignment=ft.MainAxisAlignment.END if es_mio else ft.MainAxisAlignment.START
        )

        # 6. Si es nuestro mensaje y tiene ID, lo guardamos
        if es_mio and mensaje_id:
            mensajes_map[mensaje_id] = estado_icon

        mensajes_lista.append(burbuja)

    # -----------------------------------------------------------------------------------
    # --- 4. HANDLERS DE SOCKETIO (DEBEN ESTAR AQUÍ, ANTES DEL SIO.ON) ---
    # -----------------------------------------------------------------------------------

    def recibir_historial(data):
        print("3. 📜 [HISTORIAL] Recibiendo el historial de mensajes.")

        historial_recibido = data
        if not isinstance(historial_recibido, list):
            print("❌ Error: Los datos de historial no son una lista de mensajes.", historial_recibido)
            return

        # --- LÓGICA DE PROCESAMIENTO (Fuera del hilo de UI) ---
        mensajes_lista.clear()
        mensajes_map.clear()

        for m in historial_recibido:
            id_val = m.get("mensaje_id")
            if id_val is not None:
                try:
                    id_val = int(id_val)
                except (ValueError, TypeError):
                    id_val = None

            agregar_burbuja(
                texto=m.get("texto"),
                emisor=m.get("emisor"),
                mensajes=mensajes_column,
                fecha=m.get("fecha"),
                usuario_logueado_id=user_id,
                leido=m.get("leido", False),
                mensaje_id=id_val
            )

        # 🚨 CRÍTICO: Función de Actualización en el Thread Principal 🚨
        def actualizar_ui():
            mensajes_column.controls.clear()
            mensajes_column.controls = mensajes_lista
            page.update()

            sio.emit("leer_mensajes", {
                "user_id": user_id,
                "other_user_id": receptor_id
            })

        # 💥 EJECUCIÓN ASÍNCRONA PARA FORZAR LA ACTUALIZACIÓN DE UI 💥
        page.run_thread(actualizar_ui)

    def mensaje_visto(data):
        id_data = data.get('mensaje_id')
        if not id_data: return

        if not isinstance(id_data, list):
            id_list = [id_data]
        else:
            id_list = id_data

        needs_update = False

        for mensaje_id_raw in id_list:
            try:
                mensaje_id = int(mensaje_id_raw)
            except (ValueError, TypeError):
                continue

            if mensaje_id in mensajes_map:
                icon_control = mensajes_map[mensaje_id]

                icon_control.name = ft.Icons.DONE_ALL
                icon_control.color = ft.Colors.LIGHT_BLUE_500

                needs_update = True

        if needs_update:
            # 🚨 FIX CRÍTICO DE CONDICIÓN DE CARRERA 🚨
            def forzar_actualizacion_icono():
                # Damos 200ms para que el hilo de creación del mensaje termine de mapear el icono.
                time.sleep(0.2)
                page.update()

            page.run_thread(forzar_actualizacion_icono)

    def recibir_mensaje(data):
        id_val = data.get("mensaje_id")
        if id_val is not None:
            try:
                id_val = int(id_val)
            except (ValueError, TypeError):
                id_val = None

        # ¡IMPORTANTE! Asegúrate que user_id sea un entero si lo estás usando
        try:
            user_id_int = int(user_id)
        except:
            user_id_int = user_id  # Fallback

        emisor_id = data.get("emisor")
        try:
            emisor_id_int = int(emisor_id)
        except:
            emisor_id_int = emisor_id  # Fallback

        es_mio = emisor_id_int == user_id_int

        if es_mio:
            print("2. 🔄 [ECO] Recibiendo confirmación del mensaje enviado (Server -> Cliente).")
        else:
            print("2. 📥 [RECIBIDO] Mensaje del otro usuario.")

        leido_status = data.get("leido", False)

        # 1. Agregamos la burbuja (esto actualiza mensajes_lista, no la UI)
        agregar_burbuja(
            texto=data.get("texto"),
            emisor=emisor_id,
            mensajes=mensajes_column,
            fecha=data.get("fecha"),
            usuario_logueado_id=user_id,
            leido=leido_status,
            mensaje_id=id_val
        )
        # --- 🚨 CORRECCIÓN DE THREADING 🚨 ---
        def actualizar_chat_en_tiempo_real():
            # 2. Reasignar la lista de controles
            mensajes_column.controls = mensajes_lista

            # 3. Forzar la actualización
            mensajes_column.update()
            page.update()  # Forzamos una actualización de página por si acaso

            # Opcional: Scroll al final
            if mensajes_column.controls:
                mensajes_column.scroll_to(offset=-1)
                mensajes_column.update()

            """if id_val and es_mio:
                # Esperamos un momento para garantizar que Flet haya dibujado el icono
                time.sleep(0.3)

                try:
                    # Verificamos si el mensaje ya tiene el estado de "leido" en la base de datos
                    # Esto requiere una función que consulte el estado de la base de datos o API

                    # O, alternativamente, asumimos que si el receptor está en el chat, el mensaje ya se leyó.

                    # La solución MÁS SIMPLE y efectiva: Forzar la lógica de "visto"
                    if id_val in mensajes_map:
                        icon_control = mensajes_map[id_val]

                        # Asumimos que si el receptor está activo, el visto debe ser inmediato
                        icon_control.name = ft.Icons.DONE_ALL
                        icon_control.color = ft.Colors.LIGHT_BLUE_500

                        page.update()  # Forzamos el redibujo del icono

                except Exception as e:
                    print(f"Error al forzar el visto inmediato: {e}")"""
        # 4. Ejecutar la actualización en el hilo principal de Flet
        page.run_thread(actualizar_chat_en_tiempo_real)
        # ------------------------------------

        # ❌ ELIMINAMOS ESTAS LÍNEAS porque ahora están dentro de run_thread:
        # mensajes_column.controls = mensajes_lista
        # mensajes_column.update()

        if not es_mio:
            sio.emit("message_seen", {
                "mensaje_id": data.get("mensaje_id"),
                "user_id": user_id
            })

    def enviar_mensaje(e):
        texto = input_field.value.strip()
        if not texto: return

        print("----------------------------------------------------------------")
        print("1. 📤 [ENVIANDO] Mensaje (Cliente -> Server).")

        if not sio.connected:
            try:
                print(f"⚠️ Intentando reconectar SocketIO con ID: {user_id}")
                sio.connect("http://127.0.0.1:5000", auth={"user_id": user_id})
            except Exception as ex:
                print(f"❌ Fallo al reconectar SocketIO: {ex}")
                return

        sio.emit("send_message", {
            "user_id": user_id, "other_user_id": receptor_id, "texto": texto
        })

        input_field.value = ""
        input_field.update()

    enviar_btn = ft.IconButton(icon=ft.Icons.SEND, on_click=enviar_mensaje)

    # ----------------------------------------------------------------------
    # --- 5. REGISTRO DE HANDLERS (Ahora todas las funciones ya existen) ---
    # ----------------------------------------------------------------------

    sio.on("chat_history", recibir_historial)
    sio.on("new_message", recibir_mensaje)
    sio.on("message_read", mensaje_visto)

    # ----------------------------------------------------------------------
    # --- 6. SOLICITUD DE HISTORIAL CON DELAY ---
    # ----------------------------------------------------------------------

    def solicitar_historial_con_delay():
        time.sleep(0.1)

        if receptor_id and sio.connected:
            print("📜 [SOLICITANDO] Historial de mensajes tras un delay.")
            sio.emit("get_history", {"user_id": user_id, "other_user_id": receptor_id})
        elif not sio.connected:
            print("⚠️ SocketIO no conectado al solicitar historial.")

    # 🚨 CLAVE: Solo llamamos a la función asíncrona una vez.
    page.run_thread(solicitar_historial_con_delay)

    # ----------------------------------------------------------------------
    # --- 7. ESTRUCTURA VISUAL Y RETORNO FINAL ---
    # ----------------------------------------------------------------------

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

    input_bar = ft.Container(
        content=ft.Row(
            controls=[input_field, enviar_btn],
            alignment=ft.MainAxisAlignment.START,
            spacing=5
        ),
        padding=ft.padding.only(left=10, right=5, top=5, bottom=5)
    )

    return ft.Column(
        controls=[
            header,
            # ✅ Layout con expansión correcta
            ft.Container(
                content=mensajes_column,
                expand=True
            ),
            ft.Divider(height=1),
            input_bar
        ],
        expand=True
    )
def mostrar_snackbar(page, mensaje, exito=True):
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

# -------------------
# Modal eliminar mensaje
# -------------------
def mostrar_modal_eliminar_mensaje(page, mensaje_id=None, chat_container=None, on_eliminar_callback=None):
    def confirmar_eliminar(e):
        modal.open = False
        page.update()

        # 🔥 Llamar al callback si existe (para eliminar de la lista visual)
        if on_eliminar_callback:
            on_eliminar_callback()

        # 🔥 Si hay un contenedor específico, eliminarlo
        if chat_container and chat_container in page.controls:
            page.controls.remove(chat_container)
            page.update()

        print(f"Mensaje {mensaje_id} eliminado (simulación frontend).")

        # ✅ SnackBar de confirmación
        mostrar_snackbar(page, "Conversación eliminada correctamente.", exito=True)

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

#OBTENER TOKEN DE SESSION
def obtener_token(page):
        return getattr(page, "session_token", None)

# -------------------
    # Modal Calificar
    # -------------------

def mostrar_modal_calificar(page, receptor_id):
    print("📨 ID del usuario a calificar:", receptor_id)
    calificacion = {"valor": 0}

    def actualizar_estrellas(valor):
        for i, estrella in enumerate(estrellas, start=1):
            if i <= valor:
                estrella.icon = ft.Icons.STAR
                estrella.icon_color = "#3EAEB1"
            else:
                estrella.icon = ft.Icons.STAR_BORDER
                estrella.icon_color = "#3EAEB1"
        calificacion["valor"] = valor
        page.update()


    # --- Guardar calificación ---
    def guardar_calificacion(e):
        # Validación: seleccionar estrellas
        if calificacion["valor"] == 0:
            mostrar_snackbar(page, "Selecciona al menos una estrella para calificar.", exito=False)
            return

        # Validación: escribir reseña
        if not reseña.value or reseña.value.strip() == "":
            mostrar_snackbar(page, "Por favor, escribe una reseña.", exito=False)
            return

        modal.open = False
        page.update()

        token = obtener_token(page)

        datos = {
            "reseña": reseña.value,
            "valor_calificacion": calificacion["valor"],
            "calificado_id": receptor_id
        }

        # Enviar calificación
        resultado = enviar_calificacion(token, datos)

        # ✅ SnackBar según resultado
        if resultado and resultado.get("success"):
            mostrar_snackbar(page, f"Calificación enviada: {calificacion['valor']} estrellas", exito=True)
        else:
            mensaje_error = resultado.get("message", "Error al enviar calificación.") if resultado else "Error de conexión."
            mostrar_snackbar(page, mensaje_error, exito=False)
    # --- Cancelar ---
    def cancelar_calificacion(e):
        modal.open = False
        page.update()

    # --- Crear estrellas ---
    estrellas = []
    for i in range(1, 6):
        estrella = ft.IconButton(
            icon=ft.Icons.STAR_BORDER,
            icon_color="#3EAEB1",
            icon_size=34,
            on_click=lambda e, v=i: actualizar_estrellas(v)
        )
        estrellas.append(estrella)

    # --- Campo de reseña ---
    reseña = ft.TextField(
        multiline=True,
        min_lines=3,
        max_lines=3,
        hint_text="Escribe una reseña",
        border="none",
        filled=True,
        fill_color="#D9D9D9",
        border_radius=15,
        text_style=ft.TextStyle(
            font_family="Oswald",
            size=14,
            color=ft.Colors.BLACK
        ),
        hint_style=ft.TextStyle(
            font_family="Oswald",
            size=14,
            weight=ft.FontWeight.W_500,
            color="#808080",
        ),
    )

    # Botones
    btn_guardar = ft.ElevatedButton(
        "Guardar",
        bgcolor="#3EAEB1",
        color=ft.Colors.WHITE,
        width=110,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        on_click=guardar_calificacion,
    )

    btn_cancelar = ft.OutlinedButton(
        "Cancelar",
        width=110,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        on_click=cancelar_calificacion,
    )

    # --- Modal ---
    modal = ft.AlertDialog(
        modal=False,
        bgcolor="#FFFFFF",
        content=ft.Container(
            width=380,
            height=260,
            bgcolor="#FFFFFF",
            border_radius=20,
            padding=ft.padding.only(top=15, bottom=15, left=20, right=20),
            content=ft.Column(
                [
                    ft.Text(
                        "Calificar usuario",
                        size=24,
                        weight="bold",
                        text_align="center",
                        color="#3EAEB1",
                        font_family="Oswald"
                    ),
                    ft.Row(
                        controls=estrellas,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0
                    ),
                    reseña,
                    ft.Row(
                        [btn_guardar, btn_cancelar],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
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
