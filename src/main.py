import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.file_handler import extract_content
from src.agent import analyze_document

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def main() -> None:
    """Punto de entrada CLI del agente.

    Parsea los argumentos de línea de comandos, extrae el contenido
    del archivo proporcionado, lo envía al agente de Big Pickle y
    guarda el resultado en un archivo Markdown en output/.
    """
    parser = argparse.ArgumentParser(
        description="Agente Gen AI que analiza especificaciones de aplicación "
                    "y determina si requieren IA avanzada."
    )
    parser.add_argument(
        "archivo",
        help="Ruta al archivo .txt o .pdf con la especificación",
    )

    args = parser.parse_args()

    try:
        logger.info("Leyendo archivo: %s", args.archivo)
        content = extract_content(args.archivo)

        if not content.strip():
            logger.error("El archivo está vacío.")
            sys.exit(1)

        logger.info("Analizando con Big Pickle...")
        result = analyze_document(content)

        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"analisis_{timestamp}.md"

        output_file.write_text(result.text, encoding="utf-8")
        logger.info("Resultado guardado en: %s", output_file)
        logger.info(
            "Tokens - entrada: %d | salida: %d | total: %d",
            result.prompt_tokens,
            result.completion_tokens,
            result.total_tokens,
        )

    except (FileNotFoundError, ValueError, EnvironmentError) as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Error inesperado: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
