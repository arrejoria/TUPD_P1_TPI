def normalizar_texto(valor):
    return str(valor).strip()


def validar_texto_obligatorio(valor, nombre_campo):
    valor_normalizado = normalizar_texto(valor)

    if not valor_normalizado:
        return False, "", f"{nombre_campo} no puede estar vacío."

    return True, valor_normalizado, ""


def parsear_entero_no_negativo(valor, nombre_campo):
    valor_normalizado = normalizar_texto(valor)

    if not valor_normalizado:
        return False, None, f"{nombre_campo} no puede estar vacío."

    try:
        numero = int(valor_normalizado)
    except ValueError:
        return False, None, f"{nombre_campo} debe ser un número entero."

    if numero < 0:
        return False, None, f"{nombre_campo} no puede ser negativo."

    return True, numero, ""


def parsear_entradas_rango(texto_minimo, texto_maximo, nombre_campo):
    minimo = None
    maximo = None

    if normalizar_texto(texto_minimo):
        exito, minimo, mensaje = parsear_entero_no_negativo(
            texto_minimo, f"{nombre_campo} mínimo"
        )
        if not exito:
            return False, (None, None), mensaje

    if normalizar_texto(texto_maximo):
        exito, maximo, mensaje = parsear_entero_no_negativo(
            texto_maximo, f"{nombre_campo} máximo"
        )
        if not exito:
            return False, (None, None), mensaje

    if minimo is not None and maximo is not None and minimo > maximo:
        return (
            False,
            (None, None),
            f"{nombre_campo} mínimo no puede ser mayor que {nombre_campo} máximo.",
        )

    return True, (minimo, maximo), ""


def formatear_mensaje(titulo, mensaje):
    return f"{titulo}: {mensaje}"


def formatear_paises(lista_paises, titulo="Países"):
    if not lista_paises:
        return f"{titulo}\nNo hay países para mostrar."

    encabezados = ["Nombre", "Población", "Superficie", "Continente"]
    filas = []

    for pais in lista_paises:
        filas.append(
            [
                str(pais["nombre"]),
                str(pais["poblacion"]),
                str(pais["superficie"]),
                str(pais["continente"]),
            ]
        )

    anchos = [len(encabezado) for encabezado in encabezados]

    for fila in filas:
        for indice, valor in enumerate(fila):
            anchos[indice] = max(anchos[indice], len(valor))

    separador = "-+-".join("-" * ancho for ancho in anchos)
    linea_encabezado = " | ".join(
        encabezado.ljust(anchos[indice]) for indice, encabezado in enumerate(encabezados)
    )

    lineas = [titulo, linea_encabezado, separador]
    for fila in filas:
        lineas.append(" | ".join(valor.ljust(anchos[indice]) for indice, valor in enumerate(fila)))

    return "\n".join(lineas)


def formatear_estadisticas(estadisticas):
    total_paises = estadisticas.get("total_paises", 0)
    lineas = ["Estadísticas", f"Total de países: {total_paises}"]

    if total_paises == 0:
        lineas.append("No hay estadísticas disponibles porque no hay países cargados.")
        return "\n".join(lineas)

    maxima_poblacion = estadisticas.get("maxima_poblacion")
    minima_poblacion = estadisticas.get("minima_poblacion")

    lineas.extend(
        [
            f"Mayor población: {maxima_poblacion['nombre']} ({maxima_poblacion['poblacion']})",
            f"Menor población: {minima_poblacion['nombre']} ({minima_poblacion['poblacion']})",
            f"Población promedio: {estadisticas.get('poblacion_promedio', 0):.2f}",
            f"Superficie promedio: {estadisticas.get('superficie_promedio', 0):.2f}",
            "Países por continente:",
        ]
    )

    for continente, cantidad in sorted(estadisticas.get("cantidad_por_continente", {}).items()):
        lineas.append(f"- {continente}: {cantidad}")

    return "\n".join(lineas)


def copiar_paises(lista_paises):
    return [pais.copy() for pais in lista_paises]


def _normalizar_nombre(nombre):
    return normalizar_texto(nombre).casefold()


def construir_pais_desde_entradas(texto_nombre, texto_poblacion, texto_superficie, texto_continente):
    exito, nombre, mensaje = validar_texto_obligatorio(texto_nombre, "Nombre")
    if not exito:
        return False, None, mensaje

    exito, poblacion, mensaje = parsear_entero_no_negativo(texto_poblacion, "Población")
    if not exito:
        return False, None, mensaje

    exito, superficie, mensaje = parsear_entero_no_negativo(texto_superficie, "Superficie")
    if not exito:
        return False, None, mensaje

    exito, continente, mensaje = validar_texto_obligatorio(texto_continente, "Continente")
    if not exito:
        return False, None, mensaje

    return True, {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }, ""


def construir_actualizacion_desde_entradas(texto_nombre, texto_poblacion, texto_superficie):
    exito, nombre, mensaje = validar_texto_obligatorio(texto_nombre, "Nombre del país")
    if not exito:
        return False, None, None, mensaje

    exito, poblacion, mensaje = parsear_entero_no_negativo(texto_poblacion, "Población")
    if not exito:
        return False, None, None, mensaje

    exito, superficie, mensaje = parsear_entero_no_negativo(texto_superficie, "Superficie")
    if not exito:
        return False, None, None, mensaje

    return True, nombre, poblacion, superficie


def buscar_indice_pais(lista_paises, nombre):
    nombre_normalizado = _normalizar_nombre(nombre)

    for indice, pais in enumerate(lista_paises):
        if _normalizar_nombre(pais["nombre"]) == nombre_normalizado:
            return indice

    return -1


def agregar_pais(lista_paises, pais):
    if buscar_indice_pais(lista_paises, pais["nombre"]) != -1:
        return False, "Ya existe un país con ese nombre."

    lista_paises.append(pais)
    return True, f"El país '{pais['nombre']}' se agregó correctamente."


def actualizar_pais(lista_paises, nombre, poblacion, superficie):
    indice_pais = buscar_indice_pais(lista_paises, nombre)

    if indice_pais == -1:
        return False, f"No se encontró el país '{nombre}'."

    lista_paises[indice_pais]["poblacion"] = poblacion
    lista_paises[indice_pais]["superficie"] = superficie

    return True, f"El país '{lista_paises[indice_pais]['nombre']}' se actualizó correctamente."


def buscar_paises(lista_paises, consulta, coincidencia_exacta=False):
    consulta_normalizada = _normalizar_nombre(consulta)
    resultados = []

    for pais in lista_paises:
        nombre_normalizado = _normalizar_nombre(pais["nombre"])

        if coincidencia_exacta and nombre_normalizado == consulta_normalizada:
            resultados.append(pais)
        elif not coincidencia_exacta and consulta_normalizada in nombre_normalizado:
            resultados.append(pais)

    return resultados


def _coincide_rango(valor, rango_valores):
    minimo, maximo = rango_valores

    if minimo is not None and valor < minimo:
        return False

    if maximo is not None and valor > maximo:
        return False

    return True


def filtrar_paises(
    lista_paises,
    continente=None,
    rango_poblacion=(None, None),
    rango_superficie=(None, None),
):
    continente_normalizado = normalizar_texto(continente).casefold()
    resultados = []

    for pais in lista_paises:
        if (
            continente_normalizado
            and normalizar_texto(pais["continente"]).casefold() != continente_normalizado
        ):
            continue

        if not _coincide_rango(pais["poblacion"], rango_poblacion):
            continue

        if not _coincide_rango(pais["superficie"], rango_superficie):
            continue

        resultados.append(pais)

    return resultados


def ordenar_paises(lista_paises, nombre_campo, descendente=False):
    return sorted(lista_paises, key=lambda pais: pais[nombre_campo], reverse=descendente)


def calcular_estadisticas(lista_paises):
    if not lista_paises:
        return {
            "total_paises": 0,
            "maxima_poblacion": None,
            "minima_poblacion": None,
            "poblacion_promedio": 0,
            "superficie_promedio": 0,
            "cantidad_por_continente": {},
        }

    poblacion_total = 0
    superficie_total = 0
    cantidad_por_continente = {}
    maxima_poblacion = lista_paises[0]
    minima_poblacion = lista_paises[0]

    for pais in lista_paises:
        poblacion_total += pais["poblacion"]
        superficie_total += pais["superficie"]

        continente = pais["continente"]
        cantidad_por_continente[continente] = cantidad_por_continente.get(continente, 0) + 1

        if pais["poblacion"] > maxima_poblacion["poblacion"]:
            maxima_poblacion = pais

        if pais["poblacion"] < minima_poblacion["poblacion"]:
            minima_poblacion = pais

    return {
        "total_paises": len(lista_paises),
        "maxima_poblacion": maxima_poblacion,
        "minima_poblacion": minima_poblacion,
        "poblacion_promedio": poblacion_total / len(lista_paises),
        "superficie_promedio": superficie_total / len(lista_paises),
        "cantidad_por_continente": cantidad_por_continente,
    }
