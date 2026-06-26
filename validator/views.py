from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentUploadSerializer, DocumentDetailSerializer
from .tasks import process_document_task

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentUploadSerializer
        return DocumentDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            
            # Dispara a tarefa assíncrona no Celery
            process_document_task.delay(document.id)
            
            return Response(
                {"message": "Upload realizado com sucesso. Processamento iniciado.", "document": serializer.data},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)