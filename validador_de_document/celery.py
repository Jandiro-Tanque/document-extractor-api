import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'validador_de_document.settings')

app = Celery('validador_de_document')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()