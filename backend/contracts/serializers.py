from rest_framework import serializers
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
