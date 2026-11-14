# Renombrador de archivos por fecha

Script en Python 3 (solo biblioteca estándar) que añade como prefijo la fecha de última modificación, en formato `AAAA-MM-DD_`, a los archivos de una carpeta. Fue generado por la cadena de agentes (planificador → arquitecto → constructor → auditor).

## Características

- Opera solo en el nivel superior de la carpeta; no entra en subcarpetas.
- No renombra dos veces un archivo que ya empiece con `AAAA-MM-DD_`.
- Si el nombre destino ya existe, añade un sufijo numérico (`_1`, `_2`...) antes de la extensión, sin sobrescribir nada.
- Los errores de permisos o de E/S se informan por `stderr` y no detienen el proceso.

## Uso

```powershell
python rename_files.py "C:\ruta\a\tu\carpeta"
```

## Ejemplo

Con `vacaciones.jpg` (modificado el 15/07/2023), `2023-08-01_playa.jpg` (ya renombrado) y `nota.txt` (modificado el 20/05/2022):

```text
Renombrado: 'vacaciones.jpg' -> '2023-07-15_vacaciones.jpg'
Omitido (ya renombrado): 2023-08-01_playa.jpg
Renombrado: 'nota.txt' -> '2022-05-20_nota.txt'

--- Resumen ---
Exitosos: 2
Omitidos: 1
Errores: 0
```

El orden de las líneas puede variar, porque depende del orden en que el sistema lista la carpeta.

Si ya existiera un archivo llamado `2023-07-15_vacaciones.jpg`, el script no lo sobrescribiría: renombraría el otro como `2023-07-15_vacaciones_1.jpg`.

## Notas

- Usa `st_mtime` del sistema operativo. Al copiar archivos sin preservar metadatos, esa fecha puede cambiar.
- `is_file()` sigue enlaces simbólicos, así que un enlace a un archivo se renombraría como si fuera el archivo.
- Hace falta probarlo en una carpeta de prueba antes de usarlo con archivos importantes: renombrar no tiene "deshacer".
