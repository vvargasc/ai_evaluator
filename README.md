# AI Evaluator

Agente de Gen AI construido con Big Pickle (OpenCode Zen) que analiza especificaciones de aplicaciones y determina si requieren Generative AI, Machine Learning o automatización tradicional.

## Funcionalidad

El agente recibe un archivo (`.txt` o `.pdf`) con una especificación de aplicación y evalúa:

1. Si la aplicación requiere **Generative AI**, **Machine Learning** o **automatización tradicional**.
2. Si la solución es **híbrida** (mezcla de metodologías).
3. Una **calificación** (Alta / Media / Baja) del nivel de necesidad de IA avanzada.
4. Una **justificación** basada en criterios como complejidad de datos, personalización, escalabilidad, interacción con usuarios y valor agregado de la IA.

### Criterios de evaluación

| Criterio | Gen AI | Machine Learning | Automatización | Híbrida |
| --- | --- | --- | --- | --- |
| **Tipo de datos** | Texto libre, imágenes, audio, video | Datos estructurados o semi-estructurados | Datos repetitivos y reglas claras | Mezcla de datos complejos y reglas |
| **Objetivo principal** | Generar contenido nuevo | Predecir, clasificar, recomendar | Ejecutar tareas repetitivas y reglas fijas | Combinar predicción con generación o reglas |
| **Complejidad** | Alta: modelos grandes y contextuales | Media-Alta: entrenamiento con datos históricos | Baja: reglas predefinidas | Alta: integra varios enfoques |
| **Interacción con usuarios** | Conversación natural, creatividad | Decisiones basadas en patrones | Procesos internos sin interacción compleja | Interacción variada con diferentes niveles |

## Estructura del proyecto

```
ai_evaluator/
├── src/
│   ├── __init__.py        # Package marker
│   ├── main.py            # Entry point CLI
│   ├── agent.py           # Agente Big Pickle (OpenCode Zen)
│   ├── file_handler.py    # Lectura de archivos TXT y PDF
│   └── config.py          # API key y carga del prompt
├── prompts/
│   └── prompt.txt         # Prompt del sistema para Big Pickle
├── output/                # Resultados generados (auto-creado)
├── examples/              # Archivos de ejemplo para probar
├── requirements.txt       # Dependencias del proyecto
├── .env.example           # Plantilla de variables de entorno
├── LICENSE                # Licencia MIT
└── CHANGELOG.md           # Historial de cambios
```

### Descripción de módulos

| Módulo | Responsabilidad |
| --- | --- |
| `config.py` | Carga la `OPENCODE_API_KEY` desde `.env`, define endpoint y modelo, y lee el prompt |
| `file_handler.py` | Extrae contenido de archivos `.txt` (lectura directa) y `.pdf` (vía pdfplumber) |
| `agent.py` | Configura el cliente OpenAI compatible con OpenCode Zen y envía el documento para análisis con `big-pickle` |
| `main.py` | CLI que orquesta el flujo: lectura → análisis → guardado en `output/` |

## Dependencias

| Paquete | Versión | Propósito |
| --- | --- | --- |
| `openai` | >= 1.0.0 | Cliente OpenAI compatible con OpenCode Zen |
| `python-dotenv` | >= 1.0.0 | Carga de variables de entorno desde `.env` |
| `pdfplumber` | >= 0.11.0 | Extracción de texto de archivos PDF |

## Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar la API key

Obtener una API key gratuita en [OpenCode Zen](https://opencode.ai/docs/zen) y crear el archivo `.env`:

```bash
cp .env.example .env
```

Editar `.env`:

```
OPENCODE_API_KEY=tu_api_key_aquí
```

Alternativamente, exportar la variable de entorno:

```bash
export OPENCODE_API_KEY=tu_api_key_aquí
```

## Uso

```bash
# Analizar un archivo de texto
python src/main.py documento.txt

# Analizar un archivo PDF
python src/main.py documento.pdf
```

### Ejemplo de salida

```
📄 Leyendo archivo: documento.txt
🔍 Analizando con Big Pickle...

✅ Resultado guardado en: output/analisis_20250712_143022.md
```

Los resultados se guardan en la carpeta `output/` con el formato `analisis_YYYYMMDD_HHMMSS.md`.

## Personalización

El prompt del agente se encuentra en `prompts/prompt.txt`. Puede modificarse para ajustar los criterios de evaluación, el formato de salida o el rol del agente sin alterar el código.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).
