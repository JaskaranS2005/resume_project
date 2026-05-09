# Trigger reload for PyPDF2
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from docx import Document
except ImportError:
    Document = None


def extract_pdf_text(file_path):
    if PyPDF2 is None:
        return ""

    text_chunks = []
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
        return "\n".join(text_chunks).strip()
    except Exception:
        return ""


def extract_image_text(image_path):
    if pytesseract is None or Image is None:
        return ""

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception:
        return ""


def extract_docx_text(file_path):
    if Document is None:
        return ""

    try:
        document = Document(file_path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        table_cells = []
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    value = cell.text.strip()
                    if value:
                        table_cells.append(value)
        return "\n".join([*paragraphs, *table_cells]).strip()
    except Exception:
        return ""
