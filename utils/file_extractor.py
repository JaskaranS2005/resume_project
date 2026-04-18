import fitz  # PyMuPDF

def extract_pdf_text(file_path):
    text = ""
    
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text.strip()
    
    except Exception as e:
        print("Error reading PDF:", e)
        return ""
import pytesseract
from PIL import Image

def extract_image_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print("Error reading image:", e)
        return ""
