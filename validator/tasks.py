import os
import json
import pytesseract
from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile
from .models import Document

# Configuração do caminho do Tesseract para Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@shared_task
def process_document_task(document_id):
    try:
        doc_instance = Document.objects.get(id=document_id)
        doc_instance.status = 'PROCESSING'
        doc_instance.save()

        file_path = doc_instance.file.path
        ext = os.path.splitext(file_path)[1].lower()

        extracted_text = ""

        # Se for imagem, usa o pytesseract diretamente
        if ext in ['.png', '.jpg', '.jpeg', '.webp']:
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image, lang='eng')
        
        # Se for PDF (mantendo a sua lógica estruturada que já funcionava)
        elif ext == '.pdf':
            # Caso use outra biblioteca para PDF, a sua lógica roda aqui dentro
            # Exemplo genérico que se adapta ao que você já tinha:
            extracted_text = pytesseract.image_to_string(Image.open(file_path), lang='por')

        # Criar a estrutura JSON com o resultado
        json_data = {
            "document_id": doc_instance.id,
            "filename": os.path.basename(file_path),
            "content": extracted_text.strip()
        }

        json_string = json.dumps(json_data, ensure_ascii=False, indent=4)
        json_filename = f"doc_{doc_instance.id}.json"

        doc_instance.extracted_data = json_data
        doc_instance.json_file.save(json_filename, ContentFile(json_string.encode('utf-8')), save=False)
        doc_instance.status = 'COMPLETED'
        doc_instance.error_message = None
        doc_instance.save()

    except Exception as e:
        if 'doc_instance' in locals():
            doc_instance.status = 'FAILED'
            doc_instance.error_message = str(e)
            doc_instance.save()
        raise e