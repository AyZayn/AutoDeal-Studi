from rest_framework import serializers
from .models import Contract, ClientDocument, RentalOption
from vehicles.serializers import VehicleSerializer
from users.serializers import UserSerializer


class RentalOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalOption
        fields = "__all__"


class ClientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = "__all__"
        read_only_fields = ["uploaded_at", "verified"]


class ContractSerializer(serializers.ModelSerializer):
    vehicle_detail = VehicleSerializer(source="vehicle", read_only=True)
    client_detail = UserSerializer(source="client", read_only=True)
    documents = ClientDocumentSerializer(many=True, read_only=True)
    selected_options_detail = RentalOptionSerializer(source="selected_options", many=True, read_only=True)
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=RentalOption.objects.all(),
        required=False,
    )

    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ["client", "status", "signed_at", "created_at", "updated_at"]