# Red de agentes en n8n expuesta a Claude vía MCP

Cuatro agentes (Planificador, Arquitecto, Constructor y Auditor QA) montados en un solo workflow de n8n y expuestos como herramientas MCP. Claude orquesta la cadena: llama a cada agente en orden y le pasa el resultado del anterior. Todo con herramientas gratuitas (n8n local + Gemini de Google AI Studio).

> **Repositorio complementario:** [**oficina-de-agentes-**](https://github.com/jhonni-png/oficina-de-agentes-) es una oficina 3D que visualiza en tiempo real a estos mismos cuatro agentes (Three.js + Supabase Realtime).
>
> **Misma red de agentes, otra vía:** [**opencode-pipeline**](https://github.com/jhonni-png/opencode-pipeline) ejecuta los cuatro agentes con OpenCode y modelos gratuitos, sin n8n.

## Estructura

```
claude_agents-/
├── config/
│   └── claude_desktop_config.example.json  # Ejemplo de conexión MCP para Claude Desktop
├── docs/
│   └── prueba-cadena.md                    # Resultado de la prueba de la cadena de agentes
├── examples/
│   └── renombrador/                        # Script generado por la cadena durante la prueba
├── LICENSE                                 # MIT
├── .gitignore
└── README.md
```

## Arquitectura

- **Un workflow de n8n** con un nodo *MCP Server Trigger* (path `red-agentes`), cuatro nodos *AI Agent Tool* con su System Message en español y un nodo *Gemini Chat Model* compartido.
- **Claude Desktop** se conecta al servidor MCP local mediante `mcp-remote`.
- **Orquestación:** la hace Claude, no n8n. Cada agente recibe un único campo, `Prompt__User_Message`, con la tarea y el resultado de los agentes anteriores.

## Requisitos

- Node.js (versión LTS)
- n8n (`npx n8n`, puerto 5678) con el workflow importado y **activado**
- Clave de Google AI Studio configurada como credencial en el nodo *Gemini Chat Model*
- Claude Desktop

## Configuración de Claude Desktop

Añade el servidor a `claude_desktop_config.json` (Settings → Developer → Edit Config). Hay un ejemplo en [`config/claude_desktop_config.example.json`](config/claude_desktop_config.example.json). Luego cierra Claude Desktop por completo (también desde la bandeja del sistema) y ábrelo de nuevo.

Si al abrir `http://localhost:5678/mcp/red-agentes` n8n responde 404 de "webhook no registrado" para GET y POST, esa ruta base no es el endpoint de conexión. Usa la ruta con `/sse` y `--transport sse-only`, como en el ejemplo. Comprueba siempre la *Production URL* que muestra el nodo MCP Server Trigger.

## Modelo de Gemini

- `gemini-2.5-flash` devolvió 404 ("ya no está disponible para usuarios nuevos").
- `gemini-3.8-flash` funcionó, pero devolvió 503 por alta demanda.
- Se pasó a `gemini-3.5-flash-lite`, con cuota gratuita según la página de precios de Google. Los límites reales dependen de tu proyecto: se consultan en AI Studio.
- Recomendado: activar **Retry On Fail** (3 intentos, ~5 s) en los nodos, porque hay errores transitorios (503, 429).

## Prueba de la cadena

Prompt de prueba: *"Usa planificador, arquitecto, constructor y auditor, en ese orden, para hacer un script en Python que renombre archivos por fecha. Pásale a cada uno el resultado del anterior."*

El resultado está resumido en [`docs/prueba-cadena.md`](docs/prueba-cadena.md) y el script generado está en [`examples/renombrador/`](examples/renombrador/).

## Límites conocidos

- La cuota gratuita de Gemini puede dar errores 429 con cadenas de cuatro agentes.
- El auditor puede afirmar cosas sobre el código que no están en él. Conviene pedirle en su System Message que cite la línea exacta de cada hallazgo.
- Para usar la red desde el celular hace falta un conector remoto con URL pública HTTPS (por ejemplo, un túnel de Cloudflare), con autenticación en el MCP Server Trigger. Depende del plan de Claude.

## Licencia

Distribuido bajo licencia [MIT](LICENSE).
