from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Administrateur'),
    ]

    # Champs supplémentaires en plus du User Django de base
    phone      = models.CharField(max_length=20, blank=True)       # Téléphone
    address    = models.TextField(blank=True)                       # Adresse
    city       = models.CharField(max_length=100, blank=True)       # Ville
    birth_date = models.DateField(null=True, blank=True)            # Date de naissance
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"