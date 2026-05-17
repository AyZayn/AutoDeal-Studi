from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Contract, ClientDocument, RentalOption
from .serializers import ContractSerializer, ClientDocumentSerializer, RentalOptionSerializer
import logging

logger = logging.getLogger("autodeal")


@api_view(["GET"])
@permission_classes([AllowAny])
def rental_options_list(request):
    options = RentalOption.objects.filter(is_active=True)
    serializer = RentalOptionSerializer(options, many=True)
    return Response(serializer.data)


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
        contract = serializer.save(client=self.request.user)
        logger.info(f"Nouveau dossier cree — client: {self.request.user.username} — vehicule: {contract.vehicle} — type: {contract.contract_type}")

    def destroy(self, request, *args, **kwargs):
        contract = self.get_object()
        logger.info(f"Dossier annule — client: {request.user.username} — id: {contract.id}")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser, FormParser])
    def upload_document(self, request, pk=None):
        contract = self.get_object()
        if contract.client != request.user:
            logger.warning(f"Tentative acces non autorise — user: {request.user.username} — dossier: {pk}")
            return Response({"error": "Non autorise"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClientDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract=contract)
            logger.info(f"Document uploade — type: {request.data.get('document_type')} — dossier: {pk}")
            all_types = {"cni", "justificatif_domicile", "fiche_de_paie"}
            uploaded_types = set(contract.documents.values_list("document_type", flat=True))
            if all_types.issubset(uploaded_types):
                contract.status = "documents_received"
                contract.save()
                logger.info(f"Tous les documents recus — dossier: {pk}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Erreur upload document — dossier: {pk} — erreurs: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    