from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContractViewSet, rental_options_list

router = DefaultRouter()
router.register(r"contracts", ContractViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("rental-options/", rental_options_list, name="rental-options"),
]