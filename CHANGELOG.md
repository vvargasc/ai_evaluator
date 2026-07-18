# Changelog

Todas las Notas destacadas de este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/),
y el proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.1.0] - 2026-07-18

### Agregado

- Límite de tamaño de archivo: 2 MB máximo (`MAX_FILE_SIZE_BYTES` en `config.py`).
- Límite de texto extraído: 100.000 caracteres (~25K tokens) máximo (`MAX_TEXT_LENGTH` en `config.py`).
- Timeout de 60 segundos y 2 reintentos automáticos en el cliente OpenAI.
- Sanitización del contenido del documento con delimitadores para prevenir prompt injection.

### Cambiado

- Archivo de credenciales renombrado de `.env` a `.env.local` para mayor seguridad.
- `.gitignore` ahora excluye `.env.*` (todos los archivos de entorno).
- Dependencias pinneadas a versiones exactas en `requirements.txt`.
- Errores inesperados ahora se registran sin exponer el stack trace completo.

### Actualizado

- Documentación README con nuevas secciones de límites y seguridad.
- Instrucciones de configuración actualizadas para usar `.env.local`.

## [1.0.0] - 2026-07-12

### Agregado

- Análisis de especificaciones de aplicación mediante IA (Big Pickle / OpenCode Zen).
- Soporte para archivos `.txt` y `.pdf` como entrada.
- Prompt configurable en `prompts/prompt.txt` con criterios de evaluación para Gen AI, ML, Automatización e Híbrida.
- CLI con argumentos de línea de comandos para selección de archivo.
- Guardado automático de resultados en `output/` con formato Markdown y marca de tiempo.
- Conteo de tokens de entrada, salida y total por cada análisis.
- Logging estructurado con niveles INFO, ERROR y EXCEPTION.
- Documentación completa con Google-style docstrings.
- README con descripción, estructura, dependencias, configuración y uso.
- Licencia MIT.
- Changelog siguiendo el estándar Keep a Changelog.
