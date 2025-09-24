# app/components/MenuOpciones.py
import flet as ft
from flet import Icons
from app.API_services.guardar_publicacion import guardar_publicacion
from app.API_services.eliminar_guardado import eliminar_guardado_usuario
from app.API_services.traer_guardados import traer_guardados
from app.API_services.guardar_reporte import enviar_reporte


def menu_opciones(
    page,
    modal_reporte,
    text_color="#000000",
    incluir_guardar=None,
    incluir_reporte=None,
    publicacion_id=None,
    usuario_id=None,
    on_click_opcion=None  # abrir modal de acceso
):
    items = []

    def obtener_token(page):
        return getattr(page, "session_token", None)

    token = obtener_token(page)

    # --- Opción Guardar / Eliminar ---
    if incluir_guardar and token:
        datos = {"publicacion_id": publicacion_id}

        guardados = traer_guardados(token)
        publicaciones_guardadas = [
            g["publicacion_id"] for g in guardados.get("data", [])
        ]
        ya_guardada = publicacion_id in publicaciones_guardadas

        icono = ft.Icon(
            Icons.DELETE if ya_guardada else Icons.BOOKMARK_BORDER,
            size=16,
            color="#3EAEB1",
        )
        texto = ft.Text(
            "Eliminar" if ya_guardada else "Guardar",
            color=text_color,
        )

        def toggle_guardado(e):
            nonlocal ya_guardada

            if ya_guardada:
                eliminar_guardado_usuario(token, datos)
                icono.name = Icons.BOOKMARK_BORDER
                texto.value = "Guardar"
                ya_guardada = False
            else:
                guardar_publicacion(token, datos)
                icono.name = Icons.DELETE
                texto.value = "Eliminar"
                ya_guardada = True

            page.update()  # ✅ actualizamos pero no cerramos menú

        # 👇 Usamos GestureDetector en vez de on_click directo en PopupMenuItem
        items.append(
            ft.PopupMenuItem(
                content=ft.GestureDetector(
                    on_tap=toggle_guardado,
                    content=ft.Row([icono, texto], spacing=6, alignment="start"),
                ),
                # ❌ quitamos el on_click del PopupMenuItem
            )
        )

    # --- Opción Reportar ---
    if incluir_reporte:
        items.append(
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(Icons.ERROR_OUTLINE, size=16,  color="#3EAEB1",),
                        ft.Text("Reportar", color=text_color),
                    ],
                    spacing=8,
                    alignment="start",
                ),
                on_click=lambda e: modal_reporte.show(page),
            )
        )

    # --- Si no hay sesión → icono abre modal acceso ---
    if token is None and on_click_opcion is not None:
        return ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.MORE_HORIZ,
                icon_color=text_color,
                on_click=on_click_opcion,
            ),
            width=36,
            height=36,
        )

    # --- Menú normal ---
    return ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.Icons.MORE_HORIZ,
            icon_color=text_color,
            items=items,
        ),
        width=36,
        height=36,
    )
