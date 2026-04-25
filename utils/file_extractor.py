import PyPDF2

def extract_pdf_text(file_path):
    text = ""
    
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
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
