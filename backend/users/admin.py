from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "role", "phone"]
    fieldsets = UserAdmin.fieldsets + (
        ("Informations supplementaires", {"fields": ("phone", "address", "city", "birth_date", "role")}),
    )
