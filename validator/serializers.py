from rest_framework import serializers
from .models import Document
import os

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'status', 'uploaded_at']
        read_only_fields = ['id', 'status', 'uploaded_at']

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.webp']
        if ext not in valid_extensions:
            raise serializers.ValidationError("Formato de arquivo não suportado.")
        return value

class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'status', 'extracted_data', 'json_file', 'error_message', 'uploaded_at']