# Copyright (c) 2026 AI Evaluator Contributors
# SPDX-License-Identifier: MIT

from pathlib import Path
import pdfplumber

from src.config import MAX_FILE_SIZE_BYTES


def read_text_file(path: Path) -> str:
    """Lee el contenido completo de un archivo de texto.

    Args:
        path: Ruta al archivo .txt a leer.

    Returns:
        str: Contenido del archivo codificado en UTF-8.
    """
    return path.read_text(encoding="utf-8")


def read_pdf_file(path: Path) -> str:
    """Extrae el texto de todas las páginas de un archivo PDF.

    Utiliza pdfplumber para procesar cada página y concatenar
    el texto extraído separado por líneas en blanco.

    Args:
        path: Ruta al archivo .pdf a leer.

    Returns:
        str: Texto extraído de todas las páginas del PDF,
            separado por doble salto de línea.
    """
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)


def extract_content(file_path: str) -> str:
    """Extrae el contenido de un archivo TXT o PDF.

    Valida que el archivo exista y que tenga un formato soportado
    (.txt o .pdf), luego delega la lectura a la función correspondiente.

    Args:
        file_path: Ruta al archivo a procesar.

    Returns:
        str: Contenido de texto extraído del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta indicada.
        ValueError: Si el formato del archivo no es .txt ni .pdf.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    size = path.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"Archivo demasiado grande: {size / 1024:.1f} KB. "
            f"Máximo permitido: {MAX_FILE_SIZE_BYTES / 1024:.0f} KB."
        )

    suffix = path.suffix.lower()

    if suffix == ".txt":
        return read_text_file(path)
    elif suffix == ".pdf":
        return read_pdf_file(path)
    else:
        raise ValueError(
            f"Formato no soportado: {suffix}. "
            f"Usa archivos .txt o .pdf"
        )
