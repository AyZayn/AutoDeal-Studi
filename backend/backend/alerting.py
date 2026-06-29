# backend/backend/alerting.py
import logging
from django.core.mail import send_mail
from django.conf import settings

class EmailAlertHandler(logging.Handler):
    """
    Handler de logging qui envoie un email automatiquement 
    quand une erreur critique (ERROR ou CRITICAL) se produit.
    """
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            try:
                subject = f"[AutoDeal] ALERTE {record.levelname} — {record.module}"
                
                # Récupération propre de la stacktrace / exception s'il y en a une
                exception_details = ""
                if record.exc_info:
                    import traceback
                    exception_details = "\nException / Traceback :\n" + "".join(traceback.format_exception(*record.exc_info))

                message = f"""ALERTE AUTOMATIQUE — AutoDeal

Niveau : {record.levelname}
Module : {record.module}
Fonction : {record.funcName}
Ligne : {record.lineno}
Date/Heure : {record.asctime if hasattr(record, 'asctime') else 'Instantané'}

Message :
{record.getMessage()}
{exception_details}
"""
                # Envoi de l'email en utilisant les variables de settings
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True, # Évite de faire planter l'application si le serveur mail est en panne
                )
            except Exception:
                pass