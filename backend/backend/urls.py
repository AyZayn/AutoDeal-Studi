from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger('autodeal')

class TestAlertView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        logger.error("Test d'alerte AutoDeal : le système d'alerte fonctionne !")
        return Response({"message": "L'erreur de test a été journalisée et l'e-mail a été envoyé !"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path('test-alert/', TestAlertView.as_view(), name='test-alert'), # Plus besoin d'import externe !
    path('api/', include('vehicles.urls')),
    path("api/", include("vehicles.urls")),
    path("api/", include("users.urls")),
    path("api/", include("contracts.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)