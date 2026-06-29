from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings

class TestAlertView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # On court-circuicte le logger pour tester la connexion SMTP en direct à l'écran
            send_mail(
                subject="[AutoDeal] TEST SMTP DIRECT FONCTIONNEL",
                message="Si ce message s'affiche, la connexion SMTP avec Brevo fonctionne !",
                from_email="el.abdesslam@gmail.com", # Ton adresse validée
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False, # <-- IMPORTANT : mettons False pour voir l'erreur s'il y en a une !
            )
            return Response({
                "status": "Succès SMTP", 
                "message": "Le serveur SMTP a accepté le mail en direct ! Vérifie Brevo et tes spams."
            })
        except Exception as e:
            return Response({
                "status": "Erreur de connexion SMTP",
                "erreur_technique": str(e)
            }, status=500)