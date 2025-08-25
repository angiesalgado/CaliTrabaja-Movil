import sys
import os
import flet as ft


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#  Importar vistas
from app.views.Inicio import pantalla_inicio
from app.views.menu import pantalla_menu
from app.views.categorias import pantalla_categorias
from app.views.Guardados import render_guardados  #  función de Guardados


def main(page: ft.Page):
    page.title = "Mi App"
    page.bgcolor = "#FFFFFF"
    page.scroll = "adaptive"
    page.padding = 0
    page.margin = 0
    page.spacing = 0
    page.window_maximized = True

    #  Configurar fuentes personalizadas
    page.fonts = {
        "OswaldRegular": "assets/fonts/Oswald-Regular.ttf",
        "OswaldMedium": "assets/fonts/Oswald-Medium.ttf",
        "OswaldBold": "assets/fonts/Oswald-Bold.ttf"
    }
    page.theme = ft.Theme(font_family="OswaldRegular")

    #  Función para cambiar entre pantallas
    def cambiar_pantalla(destino: str):
        page.controls.clear()
        page.bottom_appbar = None
        page.overlay.clear()  #  Limpiamos overlays (menús flotantes)
        page.update()

        if destino == "inicio":
            pantalla_inicio(page, cambiar_pantalla)
        elif destino == "menu":
            pantalla_menu(page, cambiar_pantalla)
        elif destino == "categorias":
            pantalla_categorias(page, cambiar_pantalla)
        elif destino == "guardados":  #  Ahora está bien conectado
            render_guardados(page, cambiar_pantalla)

    #  Pantalla inicial por defecto
    pantalla_inicio(page, cambiar_pantalla)


#  Para ejecutar la app y permitir acceso desde el móvil en red local
if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        host="0.0.0.0",  # Esto permite acceso desde otros dispositivos en tu red
        port=8551
    )
