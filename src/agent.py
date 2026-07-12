# Copyright (c) 2026 AI Evaluator Contributors
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from openai import OpenAI

from src.config import get_api_key, load_prompt, OPENCODE_API_BASE, MODEL_ID


@dataclass
class AnalysisResult:
    """Resultado del análisis de un documento.

    Attributes:
        text: Respuesta del modelo con el análisis.
        prompt_tokens: Cantidad de tokens de entrada.
        completion_tokens: Cantidad de tokens de salida.
        total_tokens: Total de tokens utilizados.
    """

    text: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


def get_client() -> OpenAI:
    """Crea un cliente OpenAI apuntando al endpoint de OpenCode Zen.

    Returns:
        OpenAI: Cliente configurado con la API key y base URL de OpenCode.
    """
    return OpenAI(
        api_key=get_api_key(),
        base_url=OPENCODE_API_BASE,
    )


def analyze_document(content: str) -> AnalysisResult:
    """Analiza un documento utilizando el modelo Big Pickle.

    Carga el prompt del sistema y envía el contenido del documento
    para su análisis según los criterios definidos en el prompt.

    Args:
        content: Texto extraído del documento a analizar.

    Returns:
        AnalysisResult: Objeto con el texto del análisis y el conteo
            de tokens de entrada, salida y total.

    Raises:
        openai.APIError: Si la llamada a la API de OpenCode Zen falla.
    """
    client = get_client()
    system_prompt = load_prompt()

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Analiza la siguiente especificación de aplicación:\n\n{content}",
            },
        ],
    )

    usage = response.usage

    return AnalysisResult(
        text=response.choices[0].message.content,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )
