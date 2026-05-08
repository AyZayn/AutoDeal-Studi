from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, register, profile, update_profile

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
]
