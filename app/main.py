import sys
import os
import flet as ft

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#  Importar vistas
from app.views.Inicio import pantalla_inicio
from app.views.menu import pantalla_menu
from app.views.categorias import pantalla_categorias
from app.views.mensajes import pantalla_mensajes
from app.views.Guardados import render_guardados
from app.views.publicaciones import publicaciones
from app.views.inicio_sesion import inicio_sesion
from app.views.registrarse import pantalla_registro
from app.views.recuperar_contrasena import recuperar_contrasena
from app.views.cambiar_contrasena import cambiar_contrasena
def main(page: ft.Page):
    page.title = "Mi App"
    page.bgcolor = "#FFFFFF"
    page.scroll = "adaptive"
    page.padding = 0
    page.margin = 0
    page.spacing = 0
    page.window_maximized = True

    page.fonts = {
        "OswaldRegular": "assets/fonts/Oswald-Regular.ttf",
        "OswaldMedium": "assets/fonts/Oswald-Medium.ttf",
        "OswaldBold": "assets/fonts/Oswald-Bold.ttf"
    }
    page.theme = ft.Theme(font_family="OswaldRegular")

    #  Función para cambiar entre pantallas
    def cambiar_pantalla(destino: str, origen=None):
        page.controls.clear()
        page.bottom_appbar = None
        page.overlay.clear()
        page.update()

        if destino == "inicio":
            pantalla_inicio(page, cambiar_pantalla)
        elif destino == "menu":
            pantalla_menu(page, cambiar_pantalla)
        elif destino == "mensajes":
            pantalla_mensajes(page, cambiar_pantalla)
        elif destino == "categorias":
            pantalla_categorias(page, cambiar_pantalla)
        elif destino == "guardados":
            render_guardados(page, cambiar_pantalla)
        elif destino == "publicaciones":
            publicaciones(page, cambiar_pantalla, origen=origen)
        elif destino == "login":
            inicio_sesion(page, cambiar_pantalla)
        elif destino == "recuperar_contrasena":
            recuperar_contrasena(page, cambiar_pantalla)
        elif destino == "registro":
            pantalla_registro(page, cambiar_pantalla, origen=origen)
        elif destino == "cambiar_contrasena":
            cambiar_contrasena(page, cambiar_pantalla)

    #  Pantalla inicial por defecto
    pantalla_inicio(page, cambiar_pantalla)

    def route_change(e: ft.RouteChangeEvent):
        print("Ruta recibida:", page.route, page.query)

        if page.route.startswith("/cambiar_contrasena"):
            token = page.query.get("token")
            print(f"Token recibido: {token}")  # aquí luego lo mandas a la API
            cambiar_contrasena(page, cambiar_pantalla, token=token)

    page.on_route_change = route_change

    # 🔹 Iniciar en la ruta actual (por si viene de un deep link)
    page.go(page.route)



if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="0.0.0.0")
