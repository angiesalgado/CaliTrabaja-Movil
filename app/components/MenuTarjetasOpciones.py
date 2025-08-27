# app/components/MenuOpciones.py
import flet as ft
from flet import Icons


def menu_opciones(page, modal_reporte, text_color="#000000", incluir_guardar=True):

    items = []

    # Opción Guardar
    if incluir_guardar:
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
                on_click=lambda e: print("Guardar"),
            )
        )

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
            on_click=lambda e: modal_reporte.show(page),
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
