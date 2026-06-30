import archivo_csv
import paises as modulo_paises


CAMPOS_ORDENAMIENTO = {
    "1": ("nombre", "Nombre"),
    "2": ("poblacion", "Población"),
    "3": ("superficie", "Superficie"),
}


def mostrar_menu():
    print("\n=== Aplicación de consola de países ===")
    print("1. Agregar país")
    print("2. Actualizar país")
    print("3. Buscar países")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Estadísticas")
    print("7. Salir")


def _pausar():
    input("\nPresione Enter para volver al menú...")


def _imprimir_exito(message):
    print(modulo_paises.formatear_mensaje("Éxito", message))


def _imprimir_error(message):
    print(modulo_paises.formatear_mensaje("Error", message))


def _guardar_cambios(ruta_csv, paises_actualizados, paises_en_memoria):
    try:
        archivo_csv.guardar_paises(ruta_csv, paises_actualizados)
    except (OSError, ValueError) as error:
        _imprimir_error(f"No se pudo guardar el archivo CSV: {error}")
        return False

    paises_en_memoria[:] = paises_actualizados
    return True


def manejar_agregar_pais(paises, ruta_csv):
    print("\nAgregar país")
    nombre = input("Nombre: ")
    poblacion = input("Población: ")
    superficie = input("Superficie: ")
    continente = input("Continente: ")

    exito, pais, mensaje = modulo_paises.construir_pais_desde_entradas(
        nombre, poblacion, superficie, continente
    )
    if not exito:
        _imprimir_error(mensaje)
        return

    paises_actualizados = modulo_paises.copiar_paises(paises)
    exito, mensaje = modulo_paises.agregar_pais(paises_actualizados, pais)
    if not exito:
        _imprimir_error(mensaje)
        return

    if not _guardar_cambios(ruta_csv, paises_actualizados, paises):
        return

    _imprimir_exito(mensaje)


def manejar_actualizar_pais(paises, ruta_csv):
    print("\nActualizar país")
    nombre = input("Nombre del país a actualizar: ")
    poblacion = input("Nueva población: ")
    superficie = input("Nueva superficie: ")

    exito, nombre, poblacion, superficie_o_mensaje = modulo_paises.construir_actualizacion_desde_entradas(
        nombre, poblacion, superficie
    )
    if not exito:
        _imprimir_error(superficie_o_mensaje)
        return

    paises_actualizados = modulo_paises.copiar_paises(paises)
    exito, mensaje = modulo_paises.actualizar_pais(
        paises_actualizados, nombre, poblacion, superficie_o_mensaje
    )
    if not exito:
        _imprimir_error(mensaje)
        return

    if not _guardar_cambios(ruta_csv, paises_actualizados, paises):
        return

    _imprimir_exito(mensaje)


def manejar_buscar_paises(paises):
    print("\nBuscar países")
    print("1. Nombre exacto")
    print("2. Nombre parcial")

    opcion = input("Elija el modo de búsqueda: ").strip()
    if opcion not in {"1", "2"}:
        _imprimir_error("Opción de búsqueda inválida.")
        return

    exito, consulta, mensaje = modulo_paises.validar_texto_obligatorio(
        input("Texto de búsqueda: "), "Texto de búsqueda"
    )
    if not exito:
        _imprimir_error(mensaje)
        return

    resultados = modulo_paises.buscar_paises(
        paises, consulta, coincidencia_exacta=(opcion == "1")
    )
    if not resultados:
        _imprimir_error("Ningún país coincide con la búsqueda.")
        return

    print(modulo_paises.formatear_paises(resultados, "Resultados de la búsqueda"))


def manejar_filtrar_paises(paises):
    print("\nFiltrar países")
    continente = input("Continente (deje vacío para omitir): ")
    poblacion_minima = input("Población mínima (deje vacío para omitir): ")
    poblacion_maxima = input("Población máxima (deje vacío para omitir): ")
    superficie_minima = input("Superficie mínima (deje vacío para omitir): ")
    superficie_maxima = input("Superficie máxima (deje vacío para omitir): ")

    if not any(
        modulo_paises.normalizar_texto(valor)
        for valor in [
            continente,
            poblacion_minima,
            poblacion_maxima,
            superficie_minima,
            superficie_maxima,
        ]
    ):
        _imprimir_error("Ingrese al menos un criterio de filtro.")
        return

    exito, rango_poblacion, mensaje = modulo_paises.parsear_entradas_rango(
        poblacion_minima, poblacion_maxima, "población"
    )
    if not exito:
        _imprimir_error(mensaje)
        return

    exito, rango_superficie, mensaje = modulo_paises.parsear_entradas_rango(
        superficie_minima, superficie_maxima, "superficie"
    )
    if not exito:
        _imprimir_error(mensaje)
        return

    resultados = modulo_paises.filtrar_paises(
        paises,
        continente=continente,
        rango_poblacion=rango_poblacion,
        rango_superficie=rango_superficie,
    )
    if not resultados:
        _imprimir_error("Ningún país coincide con los filtros.")
        return

    print(modulo_paises.formatear_paises(resultados, "Resultados del filtro"))


def manejar_ordenar_paises(paises):
    print("\nOrdenar países")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")

    opcion_campo = input("Elija el campo por el que desea ordenar: ").strip()
    if opcion_campo not in CAMPOS_ORDENAMIENTO:
        _imprimir_error("Campo de ordenamiento inválido.")
        return

    print("1. Ascendente")
    print("2. Descendente")
    opcion_direccion = input("Elija la dirección: ").strip()
    if opcion_direccion not in {"1", "2"}:
        _imprimir_error("Dirección de ordenamiento inválida.")
        return

    nombre_campo, etiqueta_campo = CAMPOS_ORDENAMIENTO[opcion_campo]
    resultados = modulo_paises.ordenar_paises(
        paises,
        nombre_campo,
        descendente=(opcion_direccion == "2"),
    )

    print(modulo_paises.formatear_paises(resultados, f"Ordenados por {etiqueta_campo}"))


def manejar_estadisticas(paises):
    estadisticas = modulo_paises.calcular_estadisticas(paises)
    print(modulo_paises.formatear_estadisticas(estadisticas))


def ejecutar_menu(paises, ruta_csv):
    acciones = {
        "1": lambda: manejar_agregar_pais(paises, ruta_csv),
        "2": lambda: manejar_actualizar_pais(paises, ruta_csv),
        "3": lambda: manejar_buscar_paises(paises),
        "4": lambda: manejar_filtrar_paises(paises),
        "5": lambda: manejar_ordenar_paises(paises),
        "6": lambda: manejar_estadisticas(paises),
    }

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()

        if opcion == "7":
            print("¡Hasta luego!")
            break

        accion = acciones.get(opcion)
        if accion is None:
            _imprimir_error("Opción de menú inválida.")
            _pausar()
            continue

        accion()
        _pausar()
