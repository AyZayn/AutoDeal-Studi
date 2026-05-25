import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# ID car Shell Payant sous render
username = '33610'
email = 'el.abdesslam@gmail.com'
password = 'Bonjour2026.'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser créé avec succès en production !")
else:
    print("Le superuser existe déjà.")