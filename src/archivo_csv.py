import csv
import os
import tempfile
from pathlib import Path


ENCABEZADOS_CSV = ["nombre", "poblacion", "superficie", "continente"]


def asegurar_csv(ruta):
    ruta_csv = Path(ruta)
    ruta_csv.parent.mkdir(parents=True, exist_ok=True)

    if ruta_csv.exists():
        return

    with ruta_csv.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS_CSV)
        escritor.writeheader()


def _leer_texto_obligatorio(valor, nombre_campo, numero_linea):
    valor_normalizado = str(valor).strip()

    if not valor_normalizado:
        raise ValueError(
            f"Fila CSV inválida en la línea {numero_linea}: {nombre_campo} no puede estar vacío."
        )

    return valor_normalizado


def _leer_entero_no_negativo(valor, nombre_campo, numero_linea):
    valor_normalizado = str(valor).strip()

    try:
        numero = int(valor_normalizado)
    except ValueError as error:
        raise ValueError(
            f"Fila CSV inválida en la línea {numero_linea}: {nombre_campo} debe ser un número entero."
        ) from error

    if numero < 0:
        raise ValueError(
            f"Fila CSV inválida en la línea {numero_linea}: {nombre_campo} no puede ser negativo."
        )

    return numero


def _validar_columnas_fila(fila, numero_linea):
    if fila is None:
        raise ValueError(f"Fila CSV inválida en la línea {numero_linea}.")

    if None in fila:
        raise ValueError(
            f"Fila CSV inválida en la línea {numero_linea}: demasiadas columnas."
        )

    for campo in ENCABEZADOS_CSV:
        if fila.get(campo) is None:
            raise ValueError(
                f"Fila CSV inválida en la línea {numero_linea}: muy pocas columnas."
            )


def _parsear_fila(fila, numero_linea):
    _validar_columnas_fila(fila, numero_linea)

    return {
        "nombre": _leer_texto_obligatorio(fila["nombre"], "nombre", numero_linea),
        "poblacion": _leer_entero_no_negativo(fila["poblacion"], "población", numero_linea),
        "superficie": _leer_entero_no_negativo(fila["superficie"], "superficie", numero_linea),
        "continente": _leer_texto_obligatorio(fila["continente"], "continente", numero_linea),
    }


def cargar_paises(ruta):
    ruta_csv = Path(ruta)
    asegurar_csv(ruta_csv)

    with ruta_csv.open("r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        if lector.fieldnames != ENCABEZADOS_CSV:
            raise ValueError(
                "Encabezados CSV inválidos. Se esperaba: " + ",".join(ENCABEZADOS_CSV)
            )

        paises = []
        for numero_linea, fila in enumerate(lector, start=2):
            paises.append(_parsear_fila(fila, numero_linea))

    return paises


def _normalizar_pais_para_guardar(pais, numero_registro):
    try:
        nombre = _leer_texto_obligatorio(pais["nombre"], "nombre", numero_registro)
        poblacion = _leer_entero_no_negativo(pais["poblacion"], "población", numero_registro)
        superficie = _leer_entero_no_negativo(pais["superficie"], "superficie", numero_registro)
        continente = _leer_texto_obligatorio(pais["continente"], "continente", numero_registro)
    except KeyError as error:
        raise ValueError(
            f"Registro inválido para guardar en la posición {numero_registro}: falta el campo {error.args[0]}."
        ) from error

    return {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }


def guardar_paises(ruta, paises):
    ruta_csv = Path(ruta)
    ruta_csv.parent.mkdir(parents=True, exist_ok=True)

    filas = []
    for numero_registro, pais in enumerate(paises, start=1):
        filas.append(_normalizar_pais_para_guardar(pais, numero_registro))

    ruta_temporal = None

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            newline="",
            encoding="utf-8",
            dir=ruta_csv.parent,
            delete=False,
        ) as archivo_temporal:
            ruta_temporal = Path(archivo_temporal.name)
            escritor = csv.DictWriter(archivo_temporal, fieldnames=ENCABEZADOS_CSV)
            escritor.writeheader()

            for fila in filas:
                escritor.writerow(fila)

        os.replace(ruta_temporal, ruta_csv)
    except Exception:
        if ruta_temporal is not None and ruta_temporal.exists():
            ruta_temporal.unlink()
        raise
