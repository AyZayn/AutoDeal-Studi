import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from vehicles.models import Vehicle

User = get_user_model()


class TestVehicleModel(TestCase):

    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            brand="Renault",
            model="Clio",
            year=2022,
            color="Rouge",
            mileage=15000,
            vehicle_type="car",
            fuel="gasoline",
            transmission="manual",
            seats=5,
            offer_type="sale",
            sale_price=12000.00,
            is_available=True,
        )

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.brand, "Renault")
        self.assertEqual(self.vehicle.model, "Clio")
        self.assertEqual(self.vehicle.year, 2022)

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle), "Renault Clio (2022)")

    def test_vehicle_is_available(self):
        self.assertTrue(self.vehicle.is_available)

    def test_vehicle_sale_price(self):
        self.assertEqual(float(self.vehicle.sale_price), 12000.00)

    def test_vehicle_offer_type(self):
        self.assertEqual(self.vehicle.offer_type, "sale")


class TestVehicleAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin1234",
        )
        self.vehicle = Vehicle.objects.create(
            brand="Peugeot",
            model="208",
            year=2023,
            color="Bleu",
            mileage=5000,
            vehicle_type="car",
            fuel="diesel",
            transmission="automatic",
            seats=5,
            offer_type="both",
            sale_price=18000.00,
            rent_price=50.00,
            is_available=True,
        )

    def test_list_vehicles_without_auth(self):
        response = self.client.get("/api/vehicles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_vehicles_returns_data(self):
        response = self.client.get("/api/vehicles/")
        self.assertEqual(len(response.data), 1)

    def test_get_vehicle_detail(self):
        response = self.client.get(f"/api/vehicles/{self.vehicle.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["brand"], "Peugeot")

    def test_create_vehicle_without_auth(self):
        data = {"brand": "Toyota", "model": "Yaris", "year": 2021}
        response = self.client.post("/api/vehicles/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vehicle_with_auth(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "brand": "Toyota",
            "model": "Yaris",
            "year": 2021,
            "color": "Blanc",
            "mileage": 0,
            "vehicle_type": "car",
            "fuel": "hybrid",
            "transmission": "automatic",
            "seats": 5,
            "offer_type": "sale",
            "sale_price": 15000.00,
            "is_available": True,
        }
        response = self.client.post("/api/vehicles/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vehicle_filter_by_offer_type(self):
        response = self.client.get("/api/vehicles/?offer_type=both")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vehicle_search(self):
        response = self.client.get("/api/vehicles/?search=Peugeot")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        