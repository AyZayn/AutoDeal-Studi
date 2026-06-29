from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail

class TestAlertView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Envoi direct pour tester la configuration SMTP à l'écran
            send_mail(
                subject="[AutoDeal] TEST SMTP DIRECT FONCTIONNEL",
                message="Si ce message s'affiche, la connexion SMTP avec Brevo fonctionne !",
                from_email="el.abdesslam@gmail.com",  # Ton adresse validée sur Brevo
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,  # Permet d'afficher l'erreur en clair s'il y a un blocage
            )
            return Response({
                "status": "Succès SMTP", 
                "message": "Le serveur SMTP a accepté le mail en direct ! Vérifie Brevo et tes spams."
            })
        except Exception as e:
            # Si ça échoue, l'erreur exacte s'affichera ici dans ton navigateur
            return Response({
                "status": "Erreur de connexion SMTP",
                "erreur_technique": str(e)
            }, status=500)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('test-alert/', TestAlertView.as_view(), name='test-alert'),
    path("api/", include("vehicles.urls")),
    path("api/", include("users.urls")),
    path("api/", include("contracts.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)