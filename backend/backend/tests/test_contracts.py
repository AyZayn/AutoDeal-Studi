from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from vehicles.models import Vehicle
from contracts.models import Contract, ClientDocument
import datetime

User = get_user_model()


class TestContractModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="client1",
            email="client1@test.com",
            password="pass123",
        )
        self.vehicle = Vehicle.objects.create(
            brand="BMW",
            model="Serie 3",
            year=2023,
            color="Noir",
            mileage=0,
            vehicle_type="car",
            fuel="diesel",
            transmission="automatic",
            seats=5,
            offer_type="both",
            sale_price=45000.00,
            rent_price=120.00,
            is_available=True,
        )
        self.contract = Contract.objects.create(
            client=self.user,
            vehicle=self.vehicle,
            contract_type="sale",
            status="pending",
            start_date=datetime.date.today(),
            total_price=45000.00,
        )

    def test_contract_creation(self):
        self.assertEqual(self.contract.contract_type, "sale")
        self.assertEqual(self.contract.status, "pending")

    def test_contract_default_status(self):
        self.assertEqual(self.contract.status, "pending")

    def test_contract_total_price(self):
        self.assertEqual(float(self.contract.total_price), 45000.00)

    def test_contract_client(self):
        self.assertEqual(self.contract.client, self.user)

    def test_contract_vehicle(self):
        self.assertEqual(self.contract.vehicle, self.vehicle)


class TestContractAPI(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.user = User.objects.create_user(
            username="client2",
            email="client2@test.com",
            password="pass123",
        )
        self.vehicle = Vehicle.objects.create(
            brand="Audi",
            model="A3",
            year=2022,
            color="Gris",
            mileage=10000,
            vehicle_type="car",
            fuel="gasoline",
            transmission="automatic",
            seats=5,
            offer_type="rent",
            rent_price=80.00,
            is_available=True,
        )

    def test_create_contract_without_auth(self):
        data = {
            "vehicle": self.vehicle.id,
            "contract_type": "rent",
            "start_date": "2026-06-01",
            "end_date": "2026-06-07",
            "total_price": 560.00,
        }
        response = self.client_api.post("/api/contracts/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_contract_with_auth(self):
        self.client_api.force_authenticate(user=self.user)
        data = {
            "vehicle": self.vehicle.id,
            "contract_type": "rent",
            "start_date": "2026-06-01",
            "end_date": "2026-06-07",
            "total_price": 560.00,
        }
        response = self.client_api.post("/api/contracts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_contracts_filtered_by_user(self):
        self.client_api.force_authenticate(user=self.user)
        Contract.objects.create(
            client=self.user,
            vehicle=self.vehicle,
            contract_type="rent",
            start_date=datetime.date.today(),
            total_price=560.00,
        )
        response = self.client_api.get("/api/contracts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for contract in response.data:
            self.assertEqual(contract["client"], self.user.id)

    def test_delete_contract(self):
        self.client_api.force_authenticate(user=self.user)
        contract = Contract.objects.create(
            client=self.user,
            vehicle=self.vehicle,
            contract_type="rent",
            start_date=datetime.date.today(),
            total_price=560.00,
        )
        response = self.client_api.delete(f"/api/contracts/{contract.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_contract_status_default_pending(self):
        self.client_api.force_authenticate(user=self.user)
        data = {
            "vehicle": self.vehicle.id,
            "contract_type": "rent",
            "start_date": "2026-06-01",
            "total_price": 560.00,
        }
        response = self.client_api.post("/api/contracts/", data)
        self.assertEqual(response.data["status"], "pending")
        