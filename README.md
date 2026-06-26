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