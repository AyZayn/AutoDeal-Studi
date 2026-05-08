from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["brand", "model", "vehicle_type", "fuel"]
    ordering_fields = ["sale_price", "rent_price", "year", "created_at"]

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        offer_type = self.request.query_params.get("offer_type")
        vehicle_type = self.request.query_params.get("vehicle_type")
        is_available = self.request.query_params.get("is_available")
        if offer_type:
            queryset = queryset.filter(offer_type=offer_type)
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)
        if is_available:
            queryset = queryset.filter(is_available=True)
        return queryset
