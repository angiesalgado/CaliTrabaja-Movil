import flet as ft
from . import  Inicio
from app.components.menu_inferior import menu_inferior
from app.API_services.datos_usuario import obtener_datos
from app.API_services.cambiar_contraseña import cambiar_contraseña_usuario
from app.API_services.cerrar_sesion import cerrar_sesion_api
from app.API_services.deshabilitar_cuenta import deshabilitar_cuenta_usu



# ---------- FUNCIÓN GLOBAL PARA MOSTRAR SNACKBAR ----------
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

# ---------- NAV SUPERIOR DE CONFIGURACIÓN ----------
def nav_configuracion(page: ft.Page, page_width: float, titulo="Configuración", volver_callback=None):
    text_size = 24 if page_width < 400 else 28
    icon_size = 50

    return ft.SafeArea(
        top=True,
        left=False,
        right=False,
        content=ft.Container(
            width=float("inf"),
            height=80,
            bgcolor="#F5F5F5",
            padding=ft.padding.symmetric(horizontal=10),
            margin=0,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_color="#3EAEB1",
                        icon_size=icon_size,
                        on_click=volver_callback  # 🔹 Ahora usa el callback que le pasemos
                    ),
                    ft.Text(
                        titulo,
                        color="#3EAEB1",
                        size=text_size,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(width=icon_size)
                ]
            )
        )
    )


# ---------- PANTALLA PRINCIPAL DE CONFIGURACIÓN ----------
def pantalla_configuracion(page: ft.Page, cambiar_pantalla=None):


    page.controls.clear()
    page.bottom_appbar = None
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.spacing = 0

    def obtener_token(page):
        return getattr(page, "session_token", None)

    def obtener_datos_usuario(page):
        token = obtener_token(page)

        if not token:
            print("Debes iniciar sesion o registrarte")

        respuesta= obtener_datos(token)
        print(f"Datos usuario: {respuesta}")


        datos = respuesta.get("usuario")


        return {
            "primer_nombre":datos.get("nombre"),
            "rol":datos.get("rol"),
            "fecha": datos.get("fecha_registro")
        }
    datos = obtener_datos_usuario(page)
    nombre =datos.get("primer_nombre")
    fecha = datos.get("fecha")
    rol = datos.get("rol")



    # ---------- FACTORÍA CAMPOS PASSWORD ----------
    def password_field_factory():
        field = ft.TextField(
            password=True,
            can_reveal_password=False,
            width=400,
            height=50,
            bgcolor="#E0E0E0",
            border_radius=8,
            border_color="transparent",
            text_style=ft.TextStyle(color=ft.Colors.BLACK, size=16),
            cursor_color=ft.Colors.BLACK,
            selection_color="#B0BEC5",
        )
        toggle_btn = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF)

        def toggle_password(e):
            field.password = not field.password
            toggle_btn.icon = ft.Icons.VISIBILITY if not field.password else ft.Icons.VISIBILITY_OFF
            field.update()
            toggle_btn.update()

        toggle_btn.on_click = toggle_password
        field.suffix = toggle_btn
        return field

    # ---------- NAV INFERIOR ----------
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
    # ---------- SUBVISTAS ----------

    def cambiar_contrasena():
        page.controls.clear()
        page.bottom_appbar = None
        actual_field = password_field_factory()
        nueva_field = password_field_factory()
        repetir_field = password_field_factory()

        # --- VALIDACIONES DE CONTRASEÑA (como en registro) ---
        regla_6_icon = ft.Icon(name=ft.Icons.HIGHLIGHT_OFF, color="red", size=18)
        regla_6_text = ft.Text("Al menos 6 caracteres", size=14)

        regla_mayus_icon = ft.Icon(name=ft.Icons.HIGHLIGHT_OFF, color="red", size=18)
        regla_mayus_text = ft.Text("Al menos 1 letra mayúscula", size=14)

        reglas_columna = ft.Column(
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Row([regla_6_icon, regla_6_text], alignment=ft.MainAxisAlignment.START),
                ft.Row([regla_mayus_icon, regla_mayus_text], alignment=ft.MainAxisAlignment.START),
            ]
        )

        def validar_password(e=None):
            pwd = nueva_field.value or ""
            # longitud
            if len(pwd) >= 6:
                regla_6_icon.name = ft.Icons.CHECK_CIRCLE
                regla_6_icon.color = "green"
            else:
                regla_6_icon.name = ft.Icons.HIGHLIGHT_OFF
                regla_6_icon.color = "red"
            # mayúscula
            import re
            if re.search(r"[A-Z]", pwd):
                regla_mayus_icon.name = ft.Icons.CHECK_CIRCLE
                regla_mayus_icon.color = "green"
            else:
                regla_mayus_icon.name = ft.Icons.HIGHLIGHT_OFF
                regla_mayus_icon.color = "red"
            page.update()

        nueva_field.on_change = validar_password

        # --- CONFIRMACIÓN DE CONTRASEÑAS ---
        confirm_icon = ft.Icon(size=18)
        confirm_text = ft.Text("", size=14)
        confirm_row = ft.Row([confirm_icon, confirm_text], alignment=ft.MainAxisAlignment.START)

        def validar_confirmacion(e=None):
            pwd = nueva_field.value or ""
            confirm = repetir_field.value or ""
            if confirm == "":
                confirm_text.value = ""
                confirm_icon.name = None
                confirm_icon.color = None
            elif pwd == confirm:
                confirm_icon.name = ft.Icons.CHECK_CIRCLE
                confirm_icon.color = "green"
                confirm_text.value = "Las contraseñas coinciden"
            else:
                confirm_icon.name = ft.Icons.HIGHLIGHT_OFF
                confirm_icon.color = "red"
                confirm_text.value = "Las contraseñas no coinciden"
            page.update()

        repetir_field.on_change = validar_confirmacion



        # --- GUARDAR CONTRASEÑA (NO TOCAMOS BACKEND) ---
        def guardar_contraseña(e):
            token = obtener_token(page)
            if not token:
                mostrar_snackbar(page, "Debes iniciar sesión o registrarte", exito=False)
                return

            contraseña = actual_field.value.strip() if actual_field.value else None
            nueva = nueva_field.value.strip() if nueva_field.value else None
            repetir = repetir_field.value.strip() if repetir_field.value else None

            if not contraseña or not nueva or not repetir:
                mostrar_snackbar(page, "Debes ingresar todos los campos", exito=False)
                return

            if nueva != repetir:
                mostrar_snackbar(page, "Las contraseñas no coinciden", exito=False)

            datos = {
                "actual_contrasena": contraseña,
                "nueva_contrasena": nueva,
                "confirmar_contrasena": repetir
            }

            respuesta = cambiar_contraseña_usuario(token, datos)

            if respuesta.get("error"):
                mostrar_snackbar(page, respuesta["error"], exito=False)
            elif respuesta.get("message"):
                mostrar_snackbar(page, respuesta["message"], exito=True)
                Inicio.pantalla_inicio(page, cambiar_pantalla)

        # --- UI ---
        page.add(
            ft.Column(
                expand=True,
                controls=[
                    nav_configuracion(page, page.width, "Cambiar contraseña",
                                      volver_callback=lambda e: mostrar_configuracion()),
                    ft.Container(
                        expand=True,
                        width=float("inf"),
                        bgcolor="#FFFFFF",
                        padding=ft.padding.symmetric(horizontal=20, vertical=30),
                        content=ft.Column(
                            spacing=20,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.START if page.width < 500 else ft.CrossAxisAlignment.CENTER),
                            controls=[
                                ft.Text("Contraseña actual", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                actual_field,
                                ft.Text("Nueva contraseña", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                nueva_field,
                                reglas_columna,  #validación debajo de nueva
                                ft.Text("Repetir contraseña", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                repetir_field,
                                confirm_row,  # validación debajo de repetir
                                ft.Row(
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Guardar cambios",
                                            bgcolor="#3EAEB1",
                                            color="white",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                            on_click=guardar_contraseña
                                        ),
                                        ft.ElevatedButton(
                                            "Cancelar",
                                            bgcolor="#F2F2F2",
                                            color="black",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                            on_click=lambda e: mostrar_configuracion()
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        page.update()

    def eliminar_cuenta():
        page.controls.clear()
        page.bottom_appbar = None
        confirmar_field = password_field_factory()
        error_text = ft.Text(
            value="",
            color="red",
            size=14,
            visible=False  # oculto por defecto
        )

        # 🔹 Cuando el usuario escriba o borre algo en el campo
        def limpiar_error(e):
            if error_text.visible:  # Solo si el error está visible
                error_text.visible = False
                error_text.value = ""
                page.update()

        confirmar_field.on_change = limpiar_error  # 👉 se asocia aquí

        def deshabilitar_cuenta(e):
            token = obtener_token(page)
            if not token:
                mostrar_snackbar("Debes iniciar sesión o registrarte", exito=False)
                return

            contraseña = confirmar_field.value.strip() if confirmar_field.value else None
            if not contraseña:
                mostrar_snackbar("Debes ingresar la contraseña", exito=False)
                return

            # 🔹 Validar contraseña con backend
            datos = {"contrasena": contraseña}
            respuesta = deshabilitar_cuenta_usu(token, datos)

            if respuesta.get("error") or respuesta.get("success") is False:
                mostrar_snackbar(page, "Error al eliminar la cuenta", exito=False)
                return
            # 🔹 Si es correcta -> guardar y abrir modal
            page.validar_contraseña_eliminar = contraseña
            mostrar_modal_eliminar_cuenta(page, token, cambiar_pantalla)

        page.add(
            ft.Column(
                expand=True,
                controls=[
                    nav_configuracion(page, page.width, "Eliminar cuenta",
                                      volver_callback=lambda e: mostrar_configuracion()),
                    ft.Container(
                        expand=True,
                        width=float("inf"),
                        bgcolor="#FFFFFF",
                        padding=ft.padding.symmetric(horizontal=20, vertical=30),
                        content=ft.Column(
                            spacing=20,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.START if page.width < 500 else ft.CrossAxisAlignment.CENTER),
                            controls=[
                                ft.Text(
                                    "Esta acción es permanente y no se puede deshacer.\n"
                                    "Toda tu información se eliminará de forma irreversible.\n"
                                    "No podrás volver a iniciar sesión con esta cuenta.",
                                    size=16,
                                    color="#000000"
                                ),
                                ft.Text("Confirmar contraseña", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                confirmar_field,
                                error_text,
                                ft.Row(
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(
                                            "Deshabilitar cuenta",
                                            bgcolor="#3EAEB1",
                                            color="white",
                                            width=170,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                            on_click=deshabilitar_cuenta
                                        ),
                                        ft.ElevatedButton(
                                            "Cancelar",
                                            bgcolor="#F2F2F2",
                                            color="black",
                                            width=150,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                            on_click=lambda e: mostrar_configuracion()
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        page.update()

    # ---------- VISTA PRINCIPAL DE CONFIGURACIÓN ----------
    def mostrar_configuracion():
        page.controls.clear()

        header = nav_configuracion(page, page.width, "Configuración", volver_callback=lambda e: cambiar_pantalla("menu"))

        contenido = ft.Container(
            expand=True,
            width=float("inf"),
            bgcolor="#FFFFFF",
            padding=16,
            margin=ft.margin.only(top=30),
            content=ft.Column(
                scroll="auto",
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=40),
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Nombre del usuario:", size=16,
                                                weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Text(nombre, size=16, color="#000000")
                                    ],
                                    spacing=5
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Rol actual:", size=16,
                                                weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Text(rol, size=16, color="#000000")
                                    ],
                                    spacing=5
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Se unió en:", size=16,
                                                weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Text(fecha, size=16, color="#000000")
                                    ],
                                    spacing=5
                                )
                            ]
                        )
                    ),
                    ft.Divider(thickness=1, color="#000000"),
                    ft.ListTile(
                        content_padding=ft.padding.only(left=40, right=10),
                        title=ft.Text("Cambiar contraseña", color="#000000",
                                      weight=ft.FontWeight.BOLD, size=16),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#3EAEB1"),
                        on_click=lambda e: cambiar_contrasena()
                    ),
                    ft.Divider(thickness=1, color="#000000"),
                    ft.ListTile(
                        content_padding=ft.padding.only(left=40, right=10),
                        title=ft.Text("Eliminar cuenta", color="#000000",
                                      weight=ft.FontWeight.BOLD, size=16),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#3EAEB1"),
                        on_click=lambda e: eliminar_cuenta()
                    ),
                    ft.Divider(thickness=1, color="#000000"),
                ]
            )
        )

        page.add(
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[header, contenido]
                    )
                ]
            )
        )

        page.bottom_appbar = ft.BottomAppBar(
            content=menu_inferior(
                selected_index=4,
                on_bottom_nav_click=on_bottom_nav_click
            ),
            bgcolor=ft.Colors.WHITE,
            elevation=0
        )

        page.update()

    # -------- INICIO --------
    mostrar_configuracion()


def mostrar_modal_eliminar_cuenta(page, token, cambiar_pantalla):
    """Muestra modal confirmación para eliminar cuenta"""

    def confirmar_eliminacion(e):
        contraseña = getattr(page, "validar_contraseña_eliminar", None)

        datos = {"contrasena": contraseña}
        respuesta = deshabilitar_cuenta_usu(token, datos)

        if respuesta.get("error") or respuesta.get("success") is False:
            mostrar_snackbar(page, "Error al eliminar la cuenta", exito=False)
            return

        # Si fue correcto, cerramos sesión
        cerrar_sesion_api(token)
        page.session_token = None
        modal.open = False
        page.update()

        mostrar_snackbar(page, "Cuenta eliminada correctamente", exito=True)

        from . import Inicio
        page.clean()
        Inicio.pantalla_inicio(page, cambiar_pantalla)

    def cancelar(e):
        modal.open = False
        page.update()

    # Botón rojo: eliminar
    btn_eliminar = ft.ElevatedButton(
        "Eliminar cuenta",
        bgcolor="#E74C3C",
        color=ft.Colors.WHITE,
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20),
            overlay_color={"": "#C0392B"},
            text_style={"": ft.TextStyle(
                font_family="Oswald",
                size=14,
                weight=ft.FontWeight.W_600,
                color="white"
            )}
        ),
        on_click=confirmar_eliminacion,
    )

    # Botón gris: cancelar
    btn_cancelar = ft.OutlinedButton(
        "Cancelar",
        width=110,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#f8f8f8",
            color="black",
            side=ft.BorderSide(1, "#E5E5E5"),
            text_style={"": ft.TextStyle(
                font_family="Oswald",
                size=14,
                weight=ft.FontWeight.W_500,
                color="black"
            )}
        ),
        on_click=cancelar,
    )

    # Modal
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
                        "¿Seguro que quieres eliminar tu cuenta?",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align="center",
                        color="black",
                        font_family="Oswald"
                    ),
                    ft.Text(
                        "Esta acción es irreversible.",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        text_align="center",
                        bgcolor="#333",
                        font_family="Oswald"
                    ),
                    ft.Row(
                        [btn_eliminar, btn_cancelar],
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
