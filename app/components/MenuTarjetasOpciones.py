# app/components/MenuOpciones.py
import flet as ft
from flet import Icons
from app.API_services.guardar_publicacion import guardar_publicacion
from app.API_services.guardar_reporte import enviar_reporte


def menu_opciones(page, modal_reporte, text_color="#000000", incluir_guardar=None, publicacion_id=None, usuario_id=None):

    items = []

    def  obtener_token(page):
        return getattr(page, "session_token", None)

    token = obtener_token(page)
    datos={}

    if publicacion_id:
        datos["publicacion_id"] = publicacion_id



    # Opción Guardar
    if incluir_guardar ==True:
        items.append(
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.BOOKMARK_BORDER, size=14, color=text_color),
                        ft.Text("Guardar", color=text_color),
                    ],
                    spacing=6,
                    alignment="start",
                ),
                on_click=lambda e: guardar_publicacion(token, datos)
            )
        )
    # Función para reportar
    def reportar():
        def guardar_reporte(descripcion):
            token = obtener_token(page)
            datos_reporte = {
                "descripcion": descripcion,
                "reportado_id": usuario_id,
            }
            if token:
                enviar_reporte(token, datos_reporte)
            else:
                print("Debes iniciar sesión")

        modal_reporte.on_guardar = guardar_reporte
        modal_reporte.show(page)



    # Opción Reportar
    items.append(
        ft.PopupMenuItem(
            content=ft.Row(
                [
                    ft.Icon(Icons.ERROR_OUTLINE, size=16, color=text_color),
                    ft.Text("Reportar", color=text_color),
                ],
                spacing=8,
                alignment="start",
            ),
            on_click=lambda e: reportar(),
        )
    )

    return ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.Icons.MORE_HORIZ,
            icon_color=text_color,
            items=items,
        ),
        width=36,
        height=36,
    )
