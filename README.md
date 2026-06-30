# Aplicación de consola de países

Aplicación de consola en Python para gestionar países en un archivo CSV. Esta entrega corresponde al Trabajo Práctico Integrador de Programación 1.

## Camino rápido

1. Verifique que tenga Python 3 instalado.
2. Desde la raíz del proyecto, ejecute `python src/main.py`.
3. Use el menú para agregar, actualizar, buscar, filtrar, ordenar o revisar estadísticas.

Si `data/paises.csv` no existe, el programa lo crea automáticamente solo con los encabezados.

## Propósito del proyecto

- Gestionar países con un menú simple y fácil de seguir.
- Persistir los cambios en `data/paises.csv`.
- Mantener el código modular y sencillo de explicar en clase.

## Preparación y ejecución

| Paso | Acción |
|------|--------|
| 1 | Clone o descargue el repositorio. |
| 2 | Abra una terminal en la raíz del proyecto. |
| 3 | Ejecute `python src/main.py`. |
| 4 | Siga las opciones del menú en pantalla. |

## Esquema del CSV

El archivo CSV debe mantener exactamente esta estructura:

| Columna | Significado |
|---------|-------------|
| `nombre` | Nombre del país |
| `poblacion` | Población como número entero |
| `superficie` | Superficie como número entero |
| `continente` | Nombre del continente |

Fila de encabezados esperada:

```csv
nombre,poblacion,superficie,continente
```

## Opciones del menú

La aplicación incluye estas opciones:

1. Agregar país
2. Actualizar país
3. Buscar países
4. Filtrar países
5. Ordenar países
6. Estadísticas
7. Salir

## Flujos de ejemplo

### Agregar un país

1. Elija `1. Agregar país`.
2. Ingrese el nombre, la población, la superficie y el continente.
3. Confirme el mensaje de éxito.
4. Vuelva a abrir `data/paises.csv` para verificar que la nueva fila se guardó.

### Actualizar un país

1. Elija `2. Actualizar país`.
2. Ingrese el nombre de un país existente.
3. Ingrese los nuevos valores de población y superficie.
4. Confirme el mensaje de éxito y verifique la fila actualizada en el CSV.

### Buscar países

1. Elija `3. Buscar países`.
2. Seleccione búsqueda exacta o parcial.
3. Ingrese el texto a buscar.
4. Revise los resultados formateados en pantalla.

### Filtrar países

1. Elija `4. Filtrar países`.
2. Ingrese un continente, un rango de población, un rango de superficie o una combinación.
3. Revise los países coincidentes o el mensaje de error si no hay resultados.

### Ordenar y ver estadísticas

1. Elija `5. Ordenar países` para ordenar los datos por nombre, población o superficie.
2. Elija `6. Estadísticas` para revisar totales, promedios y cantidades por continente.

## Lista de verificación manual

- [ ] Ejecutar `python src/main.py` desde un clon limpio.
- [ ] Eliminar `data/paises.csv`, ejecutar el programa y confirmar que se recrea con encabezados.
- [ ] Agregar un país y confirmar que la fila se guarda.
- [ ] Actualizar un país y confirmar que solo cambian la población y la superficie.
- [ ] Probar números inválidos, campos vacíos, rangos incorrectos y países inexistentes para confirmar que los datos no cambian.

## Documentación del informe PDF

El informe académico se encuentra en `docs/report-outline.md` y cubre los
siguientes apartados, todos vinculados a los módulos del proyecto:

| Sección del informe | Módulo / Archivo relacionado |
|----------------------|------------------------------|
| Arquitectura | `src/main.py`, `src/menu.py`, `src/paises.py`, `src/archivo_csv.py` |
| Evidencia de ejecución | Capturas de pantalla de cada flujo (ver checklist en `docs/report-outline.md`) |
| Validación de datos | `src/paises.py` (validación de entradas), `src/archivo_csv.py` (validación de CSV) |
| Persistencia segura | `src/archivo_csv.py` (escritura temporal + `os.replace`) |
| Altas, actualización y búsqueda | `src/paises.py` (`agregar_pais`, `actualizar_pais`, `buscar_paises`) |
| Filtros, ordenamiento y estadísticas | `src/paises.py` (`filtrar_paises`, `ordenar_paises`, `calcular_estadisticas`) |
| Menú e interacción | `src/menu.py` (`ejecutar_menu`, `manejar_*`) |
| Orquestación e inicio | `src/main.py` (`obtener_ruta_csv`, `main`) |

### Checklist de capturas para el informe

Las siguientes ejecuciones deben capturarse como evidencia. Cada una ejercita
un módulo específico del programa:

1. Inicio del programa y menú principal — `src/main.py` + `src/menu.py`
2. Creación automática del CSV — `src/archivo_csv.py`
3. Agregar país válido — `src/paises.py` + `src/archivo_csv.py`
4. Actualizar país existente — `src/paises.py` + `src/archivo_csv.py`
5. Búsqueda exacta y parcial — `src/paises.py`
6. Filtro por continente y rangos — `src/paises.py`
7. Ordenamiento ascendente/descendente — `src/paises.py`
8. Estadísticas — `src/paises.py`
9. Rechazo de datos inválidos — `src/paises.py` + `src/archivo_csv.py`
10. Salida del programa — `src/menu.py`

## Autor

| Alumno | Rol / Contribución |
|--------|--------------------|
| Arrejoria Lucas | Implementación de menú, archivo CSV, validaciones, documentación y pruebas manuales. |

## Entrega final

| Recurso | Estado / Lugar |
|---------|----------------|
| Repositorio público | https://github.com/arrejoria/TUPD_P1_TPI |
| Informe PDF | `TPI_Programacion1_Grupo_402.pdf` (en la raíz) |
| Video demostración | https://youtu.be/A0TJYbzzZ2o |
| Archivo ZIP | `TPI_Programacion1_Individual.zip`
