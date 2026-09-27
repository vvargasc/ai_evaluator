# Copyright (c) 2026 AI Evaluator Contributors
# SPDX-License-Identifier: MIT

from pathlib import Path
import subprocess
import pdfplumber
from docx import Document
from odf.opendocument import load
from odf.text import P
from odf.table import Table, TableRow, TableCell
from odf.draw import Page

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


def read_docx_file(path: Path) -> str:
    """Extrae el texto de todas las párrafos de un archivo DOCX.

    Utiliza python-docx para procesar cada párrafo y concatenar
    el texto extraído separado por líneas en blanco.

    Args:
        path: Ruta al archivo .docx a leer.

    Returns:
        str: Texto extraído de todos los párrafos del DOCX,
            separado por doble salto de línea.
    """
    doc = Document(path)
    text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(text_parts)


def read_doc_file(path: Path) -> str:
    """Extrae el texto de un archivo DOC (formato binario legacy).

    Utiliza la herramienta `antiword` del sistema para extraer el texto.
    Si `antiword` no está disponible, intenta usar `catdoc` como alternativa.

    Args:
        path: Ruta al archivo .doc a leer.

    Returns:
        str: Texto extraído del archivo DOC.

    Raises:
        RuntimeError: Si no se encuentra una herramienta para extraer
            texto de archivos .doc (antiword o catdoc).
    """
    for tool in ["antiword", "catdoc"]:
        try:
            result = subprocess.run(
                [tool, str(path)],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    raise RuntimeError(
        "No se encontró una herramienta para leer archivos .doc. "
        "Instala 'antiword' o 'catdoc' en el sistema."
    )


def read_odt_file(path: Path) -> str:
    """Extrae el texto de todos los párrafos de un archivo ODT.

    Utiliza odfpy para procesar cada párrafo y concatenar
    el texto extraído separado por líneas en blanco.

    Args:
        path: Ruta al archivo .odt a leer.

    Returns:
        str: Texto extraído de todos los párrafos del ODT,
            separado por doble salto de línea.
    """
    doc = load(path)
    paragraphs = doc.getElementsByType(P)
    text_parts = [str(p) for p in paragraphs if str(p).strip()]
    return "\n\n".join(text_parts)


def read_ods_file(path: Path) -> str:
    """Extrae el texto de todas las celdas con contenido de un archivo ODS.

    Utiliza odfpy para procesar cada hoja, fila y celda, concatenando
    el texto extraído separado por líneas en blanco.

    Args:
        path: Ruta al archivo .ods a leer.

    Returns:
        str: Texto extraído de todas las celdas del ODS,
            separado por doble salto de línea.
    """
    doc = load(path)
    sheets = doc.getElementsByType(Table)
    text_parts = []
    for sheet in sheets:
        rows = sheet.getElementsByType(TableRow)
        for row in rows:
            cells = row.getElementsByType(TableCell)
            for cell in cells:
                cell_text = str(cell).strip()
                if cell_text:
                    text_parts.append(cell_text)
    return "\n\n".join(text_parts)


def read_odp_file(path: Path) -> str:
    """Extrae el texto de todas las diapositivas de un archivo ODP.

    Utiliza odfpy para procesar cada página y concatenar
    el texto extraído separado por líneas en blanco.

    Args:
        path: Ruta al archivo .odp a leer.

    Returns:
        str: Texto extraído de todas las diapositivas del ODP,
            separado por doble salto de línea.
    """
    doc = load(path)
    pages = doc.getElementsByType(Page)
    text_parts = []
    for page in pages:
        page_text = str(page).strip()
        if page_text:
            text_parts.append(page_text)
    return "\n\n".join(text_parts)


def extract_content(file_path: str) -> str:
    """Extrae el contenido de un archivo TXT, PDF, DOCX, DOC, ODT, ODS u ODP.

    Valida que el archivo exista y que tenga un formato soportado
    (.txt, .pdf, .docx, .doc, .odt, .ods u .odp), luego delega la
    lectura a la función correspondiente.

    Args:
        file_path: Ruta al archivo a procesar.

    Returns:
        str: Contenido de texto extraído del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta indicada.
        ValueError: Si el formato del archivo no es soportado.
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
    elif suffix == ".docx":
        return read_docx_file(path)
    elif suffix == ".doc":
        return read_doc_file(path)
    elif suffix == ".odt":
        return read_odt_file(path)
    elif suffix == ".ods":
        return read_ods_file(path)
    elif suffix == ".odp":
        return read_odp_file(path)
    else:
        raise ValueError(
            f"Formato no soportado: {suffix}. "
            f"Usa archivos .txt, .pdf, .docx, .doc, .odt, .ods u .odp"
        )
