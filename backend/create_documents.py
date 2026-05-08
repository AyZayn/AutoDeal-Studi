import os

# Modèle Document dans contracts/models.py
contracts_models = """from django.db import models
from vehicles.models import Vehicle
from users.models import CustomUser


class Contract(models.Model):

    CONTRACT_TYPE_CHOICES = [
        ("sale", "Vente"),
        ("rent", "Location"),
    ]

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("documents_received", "Documents recus"),
        ("under_review", "En verification"),
        ("approved", "Approuve"),
        ("rejected", "Refuse"),
        ("completed", "Termine"),
        ("cancelled", "Annule"),
    ]

    client = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="contracts")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name="contracts")

    contract_type = models.CharField(max_length=10, choices=CONTRACT_TYPE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dossier {self.contract_type} - {self.vehicle} - {self.client}"

    class Meta:
        ordering = ["-created_at"]


class ClientDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ("cni", "Carte Nationale d Identite"),
        ("justificatif_domicile", "Justificatif de domicile"),
        ("fiche_de_paie", "Fiche de paie"),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.document_type} - {self.contract}"
"""

# Serializer
contracts_serializers = """from rest_framework import serializers
from .models import Contract, ClientDocument
from vehicles.serializers import VehicleSerializer
from users.serializers import UserSerializer


class ClientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = "__all__"
        read_only_fields = ["uploaded_at", "verified"]


class ContractSerializer(serializers.ModelSerializer):
    vehicle_detail = VehicleSerializer(source="vehicle", read_only=True)
    client_detail = UserSerializer(source="client", read_only=True)
    documents = ClientDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ["client", "status", "signed_at", "created_at", "updated_at"]
"""

# Views
contracts_views = """from rest_framework import viewsets, status
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
"""

# URLs
contracts_urls = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContractViewSet

router = DefaultRouter()
router.register(r"contracts", ContractViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
"""

# Admin
contracts_admin = """from django.contrib import admin
from .models import Contract, ClientDocument


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ["client", "vehicle", "contract_type", "status", "total_price", "start_date"]
    list_filter = ["contract_type", "status"]
    search_fields = ["client__username", "vehicle__brand"]
    list_editable = ["status"]


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ["contract", "document_type", "uploaded_at", "verified"]
    list_editable = ["verified"]
"""

files = {
    os.path.join("contracts", "models.py"): contracts_models,
    os.path.join("contracts", "serializers.py"): contracts_serializers,
    os.path.join("contracts", "views.py"): contracts_views,
    os.path.join("contracts", "urls.py"): contracts_urls,
    os.path.join("contracts", "admin.py"): contracts_admin,
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK " + path)

print("")
print("Backend documents mis a jour avec succes !")