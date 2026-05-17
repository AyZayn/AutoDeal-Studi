from django.db import models
from vehicles.models import Vehicle
from users.models import CustomUser


class RentalOption(models.Model):

    BILLING_TYPE_CHOICES = [
        ("monthly", "Mensuel"),
        ("one_time", "Forfait unique"),
    ]

    OPTION_TYPE_CHOICES = [
        ("included", "Inclus"),
        ("supplement", "Supplement"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    option_type = models.CharField(max_length=20, choices=OPTION_TYPE_CHOICES, default="supplement")
    billing_type = models.CharField(max_length=20, choices=BILLING_TYPE_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.option_type})"

    class Meta:
        ordering = ["option_type", "name"]


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
    selected_options = models.ManyToManyField(RentalOption, blank=True, related_name="contracts")
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