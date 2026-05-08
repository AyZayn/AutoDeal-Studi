from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Contract, ClientDocument
from .serializers import ContractSerializer, ClientDocumentSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Contract.objects.all()
        return Contract.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser, FormParser])
    def upload_document(self, request, pk=None):
        contract = self.get_object()
        if contract.client != request.user:
            return Response({"error": "Non autorise"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClientDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract=contract)
            all_types = {"cni", "justificatif_domicile", "fiche_de_paie"}
            uploaded_types = set(contract.documents.values_list("document_type", flat=True))
            if all_types.issubset(uploaded_types):
                contract.status = "documents_received"
                contract.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
