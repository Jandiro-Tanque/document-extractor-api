from django.db import models
import os

def upload_to_path(instance, filename):
    return os.path.join('documents', filename)

class Document(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PROCESSING', 'Processando'),
        ('COMPLETED', 'Concluído'),
        ('FAILED', 'Falhou'),
    ]

    file = models.FileField(upload_to=upload_to_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    extracted_data = models.JSONField(null=True, blank=True)
    json_file = models.FileField(upload_to='extracted_jsons/', null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Doc {self.id} - {self.status}"