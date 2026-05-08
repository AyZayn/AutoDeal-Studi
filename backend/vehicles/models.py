from django.db import models


class Vehicle(models.Model):

    OFFER_TYPE_CHOICES = [
        ('sale', 'Vente'),
        ('rent', 'Location'),
        ('both', 'Vente et Location'),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('car', 'Voiture'),
        ('motorcycle', 'Moto'),
        ('van', 'Utilitaire'),
        ('truck', 'Camion'),
    ]

    FUEL_CHOICES = [
        ('gasoline', 'Essence'),
        ('diesel', 'Diesel'),
        ('electric', 'Électrique'),
        ('hybrid', 'Hybride'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Manuelle'),
        ('automatic', 'Automatique'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    mileage = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='car')
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES, default='gasoline')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    seats = models.IntegerField(default=5)

    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES, default='sale')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rent_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    class Meta:
        ordering = ['-created_at']