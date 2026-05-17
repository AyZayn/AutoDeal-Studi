from django.contrib import admin
from .models import Contract, ClientDocument, RentalOption


@admin.register(RentalOption)
class RentalOptionAdmin(admin.ModelAdmin):
    list_display = ["name", "option_type", "billing_type", "price", "is_active"]
    list_editable = ["price", "is_active"]
    list_filter = ["option_type", "billing_type", "is_active"]


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