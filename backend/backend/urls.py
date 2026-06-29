from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('test-alert/', TestAlertView.as_view(), name='test-alert'), # <-- À mettre ici à la racine principale
    path('api/', include('vehicles.urls')),
    path("api/", include("vehicles.urls")),
    path("api/", include("users.urls")),
    path("api/", include("contracts.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
