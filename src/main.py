from pathlib import Path

import archivo_csv
import menu
import paises


def obtener_ruta_csv():
    return Path(__file__).resolve().parent.parent / "data" / "paises.csv"


def main():
    ruta_csv = obtener_ruta_csv()

    try:
        lista_paises = archivo_csv.cargar_paises(ruta_csv)
    except (OSError, ValueError) as error:
        print(paises.formatear_mensaje("Error", str(error)))
        print("El programa se detuvo para evitar usar datos inválidos.")
        return

    print("Los datos de países se cargaron correctamente.")
    menu.ejecutar_menu(lista_paises, ruta_csv)


if __name__ == "__main__":
    main()
