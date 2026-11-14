# Prueba de la cadena de agentes

**Tarea:** script en Python que renombre archivos de una carpeta por su fecha de modificación.
**Orquestación:** Claude llamó a los agentes en orden y pasó a cada uno el resultado del anterior.
**Modelo:** Gemini (`gemini-3.5-flash-lite` en la última prueba).

## 1. Planificador

Entregó objetivo, supuestos (nivel superior, `mtime`, formato `AAAA-MM-DD_Nombre.ext`), un plan en 4 pasos, riesgos (duplicados, permisos, subcarpetas) y criterios de aceptación.

## 2. Arquitecto

Aceptó el plan y definió: biblioteca estándar (`pathlib`, `datetime`, `argparse`), estructura de archivos, cuatro funciones (`obtener_fecha_modificacion`, `generar_nombre_unico`, `renombrar_archivos_directorio`, `main`), flujo de datos y puntos delicados (separar `stem`/`suffix`, evitar doble prefijo con regex).

## 3. Constructor

Entregó `rename_files.py` y un README. El código está en [`examples/renombrador/`](../examples/renombrador/). El README original salió con bloques de código mal cerrados y secciones repetidas; en este repositorio se dejó una versión limpia.

## 4. Auditor QA

Veredicto: **aprobado con cambios**, sin errores críticos. Criterios de aceptación cumplidos.

Revisión posterior de sus hallazgos:

- Recomendó `for elemento in list(directorio.iterdir())`, atribuyendo al código un `list(...)` que no tiene. La recomendación es válida, pero la afirmación sobre el código era inexacta.
- Afirmó que los enlaces simbólicos quedan excluidos. No es así: `is_file()` los sigue.
- No señaló el README mal formado, pese a pedírselo.

**Mejora sugerida:** pedir al auditor, en su System Message, que cite la línea exacta de cada hallazgo y que revise también la documentación.

## Incidencias durante la prueba

| Incidencia | Causa | Solución |
|---|---|---|
| 404 en `gemini-2.5-flash` | Modelo restringido a usuarios que ya lo usaban | Cambiar de modelo |
| 503 en `gemini-3.8-flash` | Alta demanda | Probar `gemini-3.5-flash-lite` y activar Retry On Fail |
| Error genérico del conector en la primera llamada | Posible reinicio de la conexión al reactivar el workflow | Reintentar |
| 404 al probar `/mcp/red-agentes` con GET y POST | La ruta base no es el endpoint de conexión | Usar `/mcp/red-agentes/sse` con `--transport sse-only` |
