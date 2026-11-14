#!/usr/bin/env python3
"""Script para renombrar archivos de una carpeta añadiendo un prefijo con su fecha de modificación (AAAA-MM-DD_)."""

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys

# Regex para detectar si un archivo ya tiene el formato AAAA-MM-DD_ al inicio
REGEX_PREFIJO_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}_")


def obtener_fecha_modificacion(ruta_archivo: Path) -> str:
    """Obtiene la fecha de modificación del archivo en formato AAAA-MM-DD.

    Lanza OSError si hay problemas de acceso.
    """
    timestamp = ruta_archivo.stat().st_mtime
    fecha = datetime.fromtimestamp(timestamp)
    return fecha.strftime("%Y-%m-%d")


def generar_nombre_unico(destino_deseado: Path) -> Path:
    """Si el archivo destino existe, añade un sufijo numérico (_1, _2, etc.)
    antes de la extensión para evitar colisiones.
    """
    if not destino_deseado.exists():
        return destino_deseado

    directorio = destino_deseado.parent
    stem = destino_deseado.stem
    suffix = destino_deseado.suffix

    contador = 1
    while True:
        nuevo_nombre = directorio / f"{stem}_{contador}{suffix}"
        if not nuevo_nombre.exists():
            return nuevo_nombre
        contador += 1


def renombrar_archivos_directorio(directorio: Path) -> None:
    """Recorre el directorio (solo nivel superior) y renombra los archivos
    añadiendo el prefijo de la fecha de modificación si no lo tienen ya.
    """
    if not directorio.is_dir():
        print(
            f"Error: '{directorio}' no es un directorio válido.",
            file=sys.stderr,
        )
        return

    print(f"Procesando directorio: {directorio.resolve()}")
    exitos = 0
    omitidos = 0
    errores = 0

    for elemento in directorio.iterdir():
        # Solo procesar archivos, ignorar carpetas
        if not elemento.is_file():
            continue

        nombre_actual = elemento.name

        # Evitar renombrar dos veces si ya tiene el prefijo AAAA-MM-DD_
        if REGEX_PREFIJO_FECHA.match(nombre_actual):
            print(f"Omitido (ya renombrado): {nombre_actual}")
            omitidos += 1
            continue

        try:
            fecha_str = obtener_fecha_modificacion(elemento)
            nuevo_nombre_base = f"{fecha_str}_{nombre_actual}"
            destino_deseado = directorio / nuevo_nombre_base

            # Resolver posibles colisiones de nombres
            destino_final = generar_nombre_unico(destino_deseado)

            elemento.rename(destino_final)
            print(f"Renombrado: '{nombre_actual}' -> '{destino_final.name}'")
            exitos += 1

        except (PermissionError, OSError) as e:
            print(
                f"Error al procesar '{nombre_actual}': {e}",
                file=sys.stderr,
            )
            errores += 1

    print("\n--- Resumen ---")
    print(f"Exitosos: {exitos}")
    print(f"Omitidos: {omitidos}")
    print(f"Errores: {errores}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Renombra archivos de una carpeta añadiendo el prefijo "
            "AAAA-MM-DD_ basado en su fecha de modificación."
        )
    )
    parser.add_argument(
        "ruta",
        type=str,
        help="Ruta de la carpeta cuyos archivos se van a renombrar.",
    )

    args = parser.parse_args()
    directorio_objetivo = Path(args.ruta)

    if not directorio_objetivo.exists():
        print(
            f"Error: La ruta '{directorio_objetivo}' no existe.", file=sys.stderr
        )
        sys.exit(1)

    if not directorio_objetivo.is_dir():
        print(
            f"Error: La ruta '{directorio_objetivo}' no es una carpeta.",
            file=sys.stderr,
        )
        sys.exit(1)

    renombrar_archivos_directorio(directorio_objetivo)


if __name__ == "__main__":
    main()
