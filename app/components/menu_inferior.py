# components/menu_inferior.py
import flet as ft

def menu_inferior(selected_index: int, on_bottom_nav_click, labels_visible=True):
    bottom_items = [
        {"icon": ft.Icons.HOME_OUTLINED, "label": "Inicio"},
        {"icon": ft.Icons.GRID_VIEW, "label": "Categorías"},
        {"icon": ft.Icons.CHAT, "label": "Mensajes"},
        {"icon": ft.Icons.BOOKMARK_OUTLINE, "label": "Guardados"},
        {"icon": ft.Icons.MENU, "label": "Menú"},
    ]

    def build_bottom_item(index, item):
        active = index == selected_index
        color = "#3EAEB1" if active else ft.Colors.BLACK

        return ft.Container(
            expand=True,
            content=ft.GestureDetector(
                on_tap=lambda e: on_bottom_nav_click(index),
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(item["icon"], color=color, size=28),
                            ft.Text(
                                item["label"],
                                size=12,
                                color=color,
                                max_lines=1,
                                visible=labels_visible,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    padding=ft.padding.symmetric(vertical=8),
                ),
            ),
        )

    return ft.Container(
        content=ft.Row(
            controls=[build_bottom_item(i, item) for i, item in enumerate(bottom_items)],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(0.5, "#3EAEB1")),
        height=70,
        padding=ft.padding.only(top=0, bottom=0, left=0, right=0),
    )
