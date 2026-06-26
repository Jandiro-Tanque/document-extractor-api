# API Validator Doc 🚀

Uma API assíncrona desenvolvida em Django REST Framework para validação e extração de dados de documentos (PDFs e Imagens) utilizando processamento em segundo plano com Celery e OCR (Optical Character Recognition).

## 🛠️ Tecnologias Utilizadas

* **Python 3.14+**
* **Django 5.2+** & **Django REST Framework** - Estrutura principal da API.
* **Celery** - Gestão e execução de tarefas assíncronas em segundo plano.
* **Upstash Redis** - Broker de mensagens e backend de resultados na nuvem (com suporte SSL).
* **Pytesseract (Tesseract OCR)** - Motor de extração de texto a partir de imagens.
* **Pillow (PIL)** - Processamento de ficheiros de imagem.

---

## 📋 Pré-requisitos (Ambiente Windows)

Para processar imagens (.png, .jpg, .jpeg), o sistema necessita do motor do Tesseract instalado no sistema operativo:

1. Transfira o instalador do Tesseract para Windows via [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
2. Durante a instalação, selecione o pacote de idioma **Portuguese** (Aditional language data) para suportar caracteres acentuados.
3. O caminho padrão de instalação deve ser: `C:\Program Files\Tesseract-OCR\tesseract.exe`.

---

## 🔧 Instalação e Configuração

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/Jandiro-Tanque/document-extractor-api
   cd "API VALIDATOR"

2. Ativar o Ambiente Virtual

.\venv\Scripts\activate

3. Instalar as dependências:


pip install -r requirements.txt

4. Executar as Migrations da Base de Dados:

python manage.py migrate


🚀 Como Executar o Projeto
O projeto necessita de dois terminais ativos concorrentemente para funcionar de forma assíncrona.

Terminal 1: Servidor Django
Inicie o servidor de desenvolvimento do Django:

Bash
python manage.py runserver
A API ficará acessível em: http://127.0.0.1:8000/

Terminal 2: Worker do Celery (Modo Windows)
Como o ambiente corre em Windows, o Celery deve ser executado utilizando o pool solo para evitar bloqueios de I/O assíncronos:

Bash
celery -A validador_de_document worker --loglevel=info -P solo

🛣️ Endpoints da API
1. Upload de Documento / Criar Tarefa
URL: /api/v1/documents/

Método: POST

Payload: multipart/form-data contendo o ficheiro no campo file.

Resposta Esperada (HTTP 202 Accepted):

JSON
{
  "message": "Upload realizado com sucesso. Processamento iniciado.",
  "document": {
    "id": 11,
    "file": "[http://127.0.0.1:8000/media/documents/exemplo.png](http://127.0.0.1:8000/media/documents/exemplo.png)",
    "status": "PENDING",
    "uploaded_at": "2026-06-26T18:08:31.327488Z"
  }
}
2. Verificar Status e Resultado do OCR
URL: /api/v1/documents/<id>/

Método: GET

Resposta (Processado com Sucesso - HTTP 200 OK):

JSON
{
  "id": 11,
  "file": "[http://127.0.0.1:8000/media/documents/exemplo.png](http://127.0.0.1:8000/media/documents/exemplo.png)",
  "status": "COMPLETED",
  "extracted_data": {
    "document_id": 11,
    "filename": "exemplo.png",
    "content": "Texto extraído pelo Tesseract OCR..."
  },
  "json_file": "[http://127.0.0.1:8000/media/extracted_jsons/doc_11.json](http://127.0.0.1:8000/media/extracted_jsons/doc_11.json)",
  "error_message": null,
  "uploaded_at": "2026-06-26T18:08:31.327488Z"
}
🧠 Fluxo de Funcionamento
O cliente faz um POST com um ficheiro (PDF ou Imagem).

O Django guarda o registo com o status PENDING e dispara uma tarefa para o broker Upstash Redis.

O Django responde imediatamente ao cliente com o HTTP 202, mantendo a aplicação fluida.

O Celery Worker deteta a nova tarefa no Redis, altera o status para PROCESSING e executa o OCR.

Após a leitura, os dados são convertidos para JSON, salvos no disco e o status é atualizado para COMPLETED.