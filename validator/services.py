import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import os

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    # 1. Tratamento para Imagens
    if ext in ['.jpg', '.jpeg', '.png', '.webp']:
        with Image.open(file_path) as img:
            extracted_text = pytesseract.image_to_string(img, lang='por')
    
    # 2. Tratamento para PDFs
    elif ext == '.pdf':
        # O 'with' garante que o fitz feche o arquivo mesmo se der erro no meio
        with fitz.open(file_path) as pdf_doc:
            for page_num in range(len(pdf_doc)):
                page = pdf_doc.load_page(page_num)
                text = page.get_text()
                
                # Se a página não tiver texto digital, aplica OCR na imagem da página
                if not text.strip():
                    pix = page.get_pixmap()
                    image_bytes = pix.tobytes("png")
                    with Image.open(io.BytesIO(image_bytes)) as img:
                        text = pytesseract.image_to_string(img, lang='por')
                
                # Consolida o texto de todas as páginas
                extracted_text += f"--- Página {page_num + 1} ---\n{text}\n"

    # Retorna o texto limpo (sem espaços inúteis no início/fim)
    return extracted_text.strip()