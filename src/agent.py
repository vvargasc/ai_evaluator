from openai import OpenAI

from src.config import get_api_key, load_prompt, OPENCODE_API_BASE, MODEL_ID


def get_client() -> OpenAI:
    """Crea un cliente OpenAI apuntando al endpoint de OpenCode Zen.

    Returns:
        OpenAI: Cliente configurado con la API key y base URL de OpenCode.
    """
    return OpenAI(
        api_key=get_api_key(),
        base_url=OPENCODE_API_BASE,
    )


def analyze_document(content: str) -> str:
    """Analiza un documento utilizando el modelo Big Pickle.

    Carga el prompt del sistema y envía el contenido del documento
    para su análisis según los criterios definidos en el prompt.

    Args:
        content: Texto extraído del documento a analizar.

    Returns:
        str: Respuesta del modelo con el análisis de la especificación,
            incluyendo tipo de solución, calificación y justificación.

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

    return response.choices[0].message.content
