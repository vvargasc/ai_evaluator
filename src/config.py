import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
PROMPT_FILE = PROMPTS_DIR / "prompt.txt"


OPENCODE_API_BASE = "https://opencode.ai/zen/v1"
MODEL_ID = "big-pickle"


def get_api_key() -> str:
    """Obtiene la API key de OpenCode Zen desde la variable de entorno.

    Carga la clave desde el archivo .env o desde la variable de entorno
    OPENCODE_API_KEY previamente exportada.

    Returns:
        str: La API key de OpenCode Zen.

    Raises:
        EnvironmentError: Si la variable OPENCODE_API_KEY no está definida.
    """
    key = os.getenv("OPENCODE_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENCODE_API_KEY no encontrada. "
            "Crea un archivo .env con tu clave o exporta la variable de entorno."
        )
    return key


def load_prompt() -> str:
    """Carga el contenido del archivo prompt.txt.

    Lee el archivo de prompt utilizado como instrucción del sistema
    para el agente de Big Pickle.

    Returns:
        str: El contenido del prompt.

    Raises:
        FileNotFoundError: Si el archivo prompt.txt no existe.
    """
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Prompt no encontrado en {PROMPT_FILE}")
    return PROMPT_FILE.read_text(encoding="utf-8")
