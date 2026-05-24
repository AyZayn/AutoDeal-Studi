from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'offer_type', 'sale_price', 'rent_price', 'is_available']
    list_filter = ['offer_type', 'vehicle_type', 'fuel', 'is_available']
    search_fields = ['brand', 'model','year']