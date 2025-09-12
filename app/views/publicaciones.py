import flet as ft
from flet import Icons
from app.components.ModalReporte import ModalReporte
from app.components.nav import nav_bar
from app.components.menu_inferior import menu_inferior
from app.components.ModalTarjetaCompleta import ModalTarjetaCompleta
from app.components.MenuTarjetasOpciones import menu_opciones
from app.API_services.traer_publicaciones import traer_publicaciones_usu

def custom_expansion(page, title, controls_list):
    toggle_icon = ft.Icon(name=ft.Icons.KEYBOARD_ARROW_DOWN, color="#3EAEB1")


    styled_controls = []
    for control in controls_list:
        if isinstance(control, ft.Radio):
            control.label_style = ft.TextStyle(
                color="#666666",
                weight=ft.FontWeight.W_500
            )
        elif isinstance(control, ft.Checkbox):
            control.label_style = ft.TextStyle(
                color="#666666",
                weight=ft.FontWeight.W_500
            )
        styled_controls.append(control)

    content_column = ft.Column(styled_controls, visible=False, spacing=5)



    def toggle_visibility(e):
        content_column.visible = not content_column.visible
        toggle_icon.name = (
            ft.Icons.KEYBOARD_ARROW_UP if content_column.visible else ft.Icons.KEYBOARD_ARROW_DOWN
        )
        page.update()

    return ft.Column(
        [
            ft.GestureDetector(
                on_tap=toggle_visibility,
                content=ft.Row(
                    [
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color="black"
                        ),
                        toggle_icon,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
            content_column
        ],
        spacing=8
    )



def publicaciones(page: ft.Page, cambiar_pantalla, origen=None):
    # ---------------- CONFIGURACIÓN GENERAL ----------------
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.theme_mode = "light"
    page.bgcolor = "#F8F8F8"
    page.title = "Inicio"
    page.scroll = ft.ScrollMode.HIDDEN
    page.padding = 1

    PRIMARY_COLOR = "#3EAEB1"
    TEXT_COLOR = "#000000"
    BORDER_COLOR = "#D9D9D9"

    #---------------------------------------------



    #------------------------------------------------------------------------------

    def obtener_token(page):
        return getattr(page, "session_token", None)

    def obtener_publicaciones(categoria_id=None, subcategoria_id=None, tiempo=None):

        datos = {}
        if categoria_id and categoria_id !="Todas":
            datos["categoria_id"] = categoria_id

        if subcategoria_id:
            datos["subcategoria_id"] = subcategoria_id

        if tiempo and tiempo !="Todas":
            datos["tiempo"] = tiempo

        publicaciones = traer_publicaciones_usu(datos)

        print(publicaciones)

        lista = []

        # Solo recorro la parte de publicaciones_generales
        for pub in publicaciones.get("publicaciones_generales", []):
            lista.append({
                "nombre": pub.get("nombre_experto"),
                "profesion": pub.get("subcategoria"),
                "descripcion": pub.get("descripcion"),
                "costo": pub.get("costo"),
                "usuario_id":pub.get("usuario_id"),
                "publicacion_id":pub.get("publicacion_id"),
                "foto_perfil": pub.get("foto_perfil")
            })

        # Devuelvo lo que necesites
        return {
            "lista": lista,
            "categorias": publicaciones.get("categorias", []),
            "total_resultados": publicaciones.get("total_resultados", 0),
            "categoria_seleccionada": publicaciones.get("categoria_selecionada")
        }

    # Si se pasó un filtro desde inicio
    if origen and "categoria_id" in origen:
        cat_id = origen["categoria_id"]
        resultado = obtener_publicaciones(categoria_id=cat_id)
    else:
        resultado = obtener_publicaciones()

    publicaciones_filtradas = resultado["lista"]




    # ---------------- REFERENCIAS PARA FILTROS ----------------
    categoria_ref = ft.Ref[ft.RadioGroup]()
    fecha_ref = ft.Ref[ft.RadioGroup]()

    # ---------------- INSTANCIA DEL MODAL ----------------
    modal_reporte = ModalReporte()
    page.overlay.append(modal_reporte.dialog)

    modal_detalle = ModalTarjetaCompleta()
    page.overlay.append(modal_detalle.dialog)

    def abrir_modal_detalle(foto_perfil,nombre, profesion, descripcion, costo, calificacion):
        print("CLICK -> abrir_modal_detalle:", nombre)  # <-- mira la consola donde corres Flet
        modal_detalle.set_content(foto_perfil,nombre, profesion, descripcion, costo, calificacion)
        page.dialog = modal_detalle.dialog
        modal_detalle.dialog.open = True
        page.update()

    # 🔹 Overlay oscuro (para cerrar al hacer clic afuera)
    overlay = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        width=page.width,
        height=page.height,
        visible=False,
        on_click=lambda e: cerrar_filtros(),
    )




    # ---------------- FUNCIONES PANEL ----------------

    def aplicar_filtros(e):
        categoria = categorias.value
        fecha = fechas.value
        print(f"Categoria seleccionada: {categoria}, fecha seleccionada: {fecha}")

        filtrar_publicaciones = obtener_publicaciones(categoria_id=categoria, subcategoria_id=None, tiempo=fecha)


        publicaciones_filtradas = filtrar_publicaciones["lista"]
        total_filtradas = len(publicaciones_filtradas)
        print(f"Publicaciones filtradas: {publicaciones_filtradas}")

        # 🔹 reconstruir el contenido del grid_column
        grid_column.controls.clear()
        for i in range(0, len(publicaciones_filtradas), 2):
            fila = ft.Container(
                content=ft.Row(
                    controls=[tarjeta_horizontal(**publicaciones_filtradas[i])] +
                             ([tarjeta_horizontal(**publicaciones_filtradas[i + 1])]
                              if i + 1 < len(publicaciones_filtradas) else []),
                    spacing=7,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=ft.padding.symmetric(horizontal=5)
            )
            grid_column.controls.append(fila)
        # 🔹 actualizar el número de resultados dinámicamente
        resultado_texto.value = f"{total_filtradas} resultados"

        page.update()
        cerrar_filtros()

    # ---------------- RADIOGROUPS PARA FILTROS ----------------


    categorias = ft.RadioGroup(
        ref=categoria_ref,
        content=ft.Column(
            [
                ft.Radio(value="Todas", label="Todas"),
                ft.Radio(value="1", label="Reparación y Mantenimiento"),
                ft.Radio(value="2", label="Cuidado y Asistencia"),
                ft.Radio(value="3", label="Bienestar de Mascotas"),
                ft.Radio(value="4", label="Educativos y aprendizaje"),
                ft.Radio(value="5", label="Hogar y Limpieza"),
                ft.Radio(value="6", label="Construcción y Remodelación"),
                ft.Radio(value="7", label="Artísticos y creatividad visual"),
                ft.Radio(value="8", label="Movilidad y transporte"),
                ft.Radio(value="9", label="Gastronomía"),
                ft.Radio(value="10", label="Eventos"),
                ft.Radio(value="11", label="Bienestar Personal"),
            ]
        )
    )

    fechas = ft.RadioGroup(
        ref=fecha_ref,
        content=ft.Column(
            [
                ft.Radio(value="Todas", label="Todas"),
                ft.Radio(value="24h", label="Últimas 24 horas"),
                ft.Radio(value="semana", label="Esta semana"),
                ft.Radio(value="mes", label="Este mes"),
            ],
            spacing=5
        )
    )
    filtros_panel = ft.Container(
        bgcolor="white",
        width=250,
        height=page.height,
        right=page.width,
        top=0,
        padding=0,
        animate_position=300,
        content=ft.Column(
            [

                # HEADER DEL PANEL
                ft.Container(
                    bgcolor="#F8F8F8",
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    content=ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                on_click=lambda e: cerrar_filtros(),
                                icon_color="#3EAEB1",
                            ),
                            ft.Text(
                                "Filtrar",
                                size=20,
                                weight=ft.FontWeight.W_500,
                                font_family="Oswald",
                                color="black"
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ),

                # CUERPO DEL PANEL
                ft.Container(
                    expand=True,
                    padding=ft.padding.all(15),
                    content=ft.Column(
                        [

                            # Categorías
                            custom_expansion(page, "Categorías", [categorias]),

                            # Fecha de publicación
                            ft.Text(
                                "Fecha de publicación",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color="black"
                            ),
                            fechas

                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO
                    )
                ),

                # BOTONES
                ft.Container(
                    content=ft.Row(
                        [
                            ft.ElevatedButton(
                                "Aplicar",
                                width=100,
                                height=40,
                                bgcolor=PRIMARY_COLOR,
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=30),
                                    padding=8
                                ),
                                on_click=aplicar_filtros
                            ),
                            ft.OutlinedButton(
                                "Limpiar filtros",
                                width=100,
                                height=40,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=30),
                                    padding=8,
                                    color="black"
                                ),
                                on_click=lambda e: (
                                    setattr(categorias, "value", None),
                                    setattr(fechas, "value", None),
                                    page.update(),
                                    print("Filtros limpiados")
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=ft.padding.only(bottom=10)
                )

            ],
            spacing=12,
        )
    )




        #custom_expansion(
        #   page,
        #"Subcategorías",
        # [
        #    ft.Checkbox(label="SubCategoría 1"),
        #   ft.Checkbox(label="SubCategoría 2"),
        #]
        #),




    def abrir_filtros(e=None):
        filtros_panel.right = page.width - 250
        overlay.visible = True
        page.update()

    def cerrar_filtros(e=None):
        filtros_panel.right = page.width  # vuelve a salir
        overlay.visible = False
        page.update()

    # ---------------- ENCABEZADO RESULTADOS ----------------
    resultado_texto = ft.Text(
        f"{len(publicaciones_filtradas)} resultados",
        weight=ft.FontWeight.BOLD,
        size=14,
        color="#666666"
    )

    # ---------------- ENCABEZADO RESULTADOS ----------------
    header_resultados = ft.Container(
        content=ft.Column(
            [
                ft.ElevatedButton(
                    "Filtros",
                    bgcolor=PRIMARY_COLOR,
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=6)
                    ),
                    on_click=abrir_filtros
                ),
                resultado_texto,
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=10,
        alignment=ft.alignment.top_left
    )

    # ---------------- PAGINACIÓN ----------------
    paginacion = ft.Container(
        content=ft.Row(
            [
                # Flecha izquierda en negro
                ft.IconButton(ft.Icons.CHEVRON_LEFT, tooltip="Anterior", icon_color=TEXT_COLOR),

                # Página activa
                ft.Container(
                    ft.Text("1", color="white"),  # círculo activo en blanco
                    bgcolor=PRIMARY_COLOR,
                    padding=6,
                    border_radius=12,
                ),
                # Páginas inactivas en negro
                ft.Container(ft.Text("2", color=TEXT_COLOR), padding=6, border_radius=12),
                ft.Container(ft.Text("3", color=TEXT_COLOR), padding=6, border_radius=12),
                ft.Container(ft.Text("4", color=TEXT_COLOR), padding=6, border_radius=12),
                ft.Container(ft.Text("...", color=TEXT_COLOR), padding=6, border_radius=12),

                # Flecha derecha en negro
                ft.IconButton(ft.Icons.CHEVRON_RIGHT, tooltip="Siguiente", icon_color=TEXT_COLOR),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        width=float("inf"),
        bgcolor="white",
        border_radius=12,
        padding=10,
        margin=ft.margin.all(8)
    )



    # ---------------- FUNCIÓN TARJETAS ----------------
    def tarjeta_horizontal(foto_perfil, nombre, profesion, descripcion, costo, usuario_id, publicacion_id, calificacion=4):
        mostrar_boton = len(descripcion) > 70

        stars = ft.Row(
            [ft.Icon(ft.Icons.STAR if i < calificacion else ft.Icons.STAR_BORDER,
                     color=PRIMARY_COLOR, size=14) for i in range(5)],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
        )
        token = obtener_token(page)

        if token == None:
            menu = menu_opciones(page, modal_reporte, incluir_guardar=False, incluir_reporte=False)
            print("Debes iniciar sesion o registrarte GUARDAR")

        else:
            # Menú con Guardar + Reportar
            menu = menu_opciones(page, modal_reporte, text_color=TEXT_COLOR, incluir_guardar=True, incluir_reporte=True,  usuario_id=usuario_id, publicacion_id=publicacion_id)

        base_url = "http://localhost:5000/static/uploads/perfiles/"

        if foto_perfil and foto_perfil.lower() != "none":
            img_url = f"{base_url}{foto_perfil}"
        else:
            img_url = f"{base_url}defecto.png"  # imagen por defecto

        # Contenido principal
        tarjeta_contenido = ft.Container(
            padding=ft.padding.only(top=10),
            content=ft.Column(
                [
                    ft.CircleAvatar(foreground_image_src=img_url, radius=30, bgcolor=ft.Colors.GREY_300),
                    ft.Text(f"COP {costo}/h", size=11, color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Text(nombre, weight=ft.FontWeight.BOLD, size=17, color=TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER),
                    stars,
                    ft.Text(profesion, size=14, weight=ft.FontWeight.W_500, color=TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Descripción:", size=12, color=ft.Colors.BLACK54, text_align=ft.TextAlign.CENTER),

                    ft.Container(
                        content=ft.Text(
                            descripcion,
                            size=11,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color=TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER
                        ),
                        height=32,
                        alignment=ft.alignment.center
                    ),

                    # Botón Ver más con cursor y on_click
                    ft.Container(
                        content=ft.TextButton(
                            "Ver más" if mostrar_boton else "",
                            on_click=(lambda e: abrir_modal_detalle(nombre, profesion, descripcion, costo,
                                                                    calificacion)) if mostrar_boton else None,
                            style=ft.ButtonStyle(
                                color=PRIMARY_COLOR if mostrar_boton else "transparent",
                                padding=0,
                                text_style=ft.TextStyle(size=11)
                            )
                        ),
                        margin=ft.margin.only(top=-3)  # 🔹 lo sube 6px
                    )

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3
            )
        )

        return ft.Container(
            width=179,
            height=270,
            padding=8,
            bgcolor="white",
            border_radius=14,
            border=ft.border.all(1, BORDER_COLOR),
            content=ft.Stack(
                controls=[
                    tarjeta_contenido,
                    ft.Container(  # 👈 ahora sí lo posicionamos aquí
                        content=menu,
                        top=5,
                        right=5,
                    ),
                ]
            )
        )




    # ---------------- GRID 2x2 ----------------
    filas = []

    grid_column = ft.Column(
        filas,
        spacing=7,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    grid_column.controls.clear()
    # 🔹 Llenar el grid con todas las publicaciones al inicio
    publicaciones = publicaciones_filtradas

    for i in range(0, len(publicaciones), 2):
        fila = ft.Container(
            content=ft.Row(
                controls=[tarjeta_horizontal(**publicaciones[i])] +
                         ([tarjeta_horizontal(**publicaciones[i + 1])]
                          if i + 1 < len(publicaciones) else []),
                spacing=7,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.symmetric(horizontal=5)
        )
        grid_column.controls.append(fila)



    # Aquí organizamos a que interfaz devuelve dependiendo de dónde vino
    back_action = lambda e: cambiar_pantalla("categorias") if origen == "categorias" else cambiar_pantalla("menu")

    # ---------------- NAV SUPERIOR + CONTENIDO ----------------
    layout = ft.Column(
        [
            nav_bar(
                page,
                page.width,
                show_back=True,
                show_explora=True,
                on_back_click=back_action
            ),
            ft.Stack(
                [
                    ft.Column(
                        [
                            header_resultados,
                            ft.Column([paginacion], alignment=ft.MainAxisAlignment.CENTER, spacing=1),
                            grid_column
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    overlay,
                    filtros_panel
                ]
            )
        ],
        spacing=10,
        expand=True
    )

    # ---------------- MENÚ INFERIOR ----------------
    selected_index = 4

    def on_bottom_nav_click(index):
        if index == 0:  # Inicio
            cambiar_pantalla("inicio")
        elif index == 1:  # Categorias
            cambiar_pantalla("categorias")
        elif index == 2:  # Mensajes
            token = obtener_token(page)
            if token:
                cambiar_pantalla("mensajes")
            else:
                print("Inicia sesion o registrate")
        elif index == 3:  # Guardados
            token = obtener_token(page)
            if token:
                cambiar_pantalla("guardados")
            else:
                print("Inicia sesion o registrate")
        elif index == 4:  # Menú
                cambiar_pantalla("menu")


    menu = menu_inferior(selected_index, on_bottom_nav_click)

    page.bottom_appbar = ft.BottomAppBar(
        content=menu,
        bgcolor=ft.Colors.WHITE,
        elevation=0,
    )

    page.add(layout)
    page.update()




