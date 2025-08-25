import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flet as ft
from app.views.inicio_sesion import inicio_sesion
from app.views.registrarse import registro


def main(page: ft.Page):
    # Configuración global
    page.title = "Mi App"
    page.bgcolor = "#FFFFFF"
    page.scroll = "adaptive"
    page.padding = 0
    page.margin = 0
    page.spacing = 0
    page.window_maximized = True

    # Cargar fuentes personalizadas
    page.fonts = {
        "OswaldRegular": "assets/fonts/Oswald-Regular.ttf",
        "OswaldMedium": "assets/fonts/Oswald-Medium.ttf",
        "OswaldBold": "assets/fonts/Oswald-Bold.ttf"
    }
    page.theme = ft.Theme(font_family="OswaldRegular")

    def go_to_login(e=None):
        inicio_sesion(page)

    def go_to_register(e=None):
        registro(page)

    #  Vista inicial corregida
    inicio_sesion(page)
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
