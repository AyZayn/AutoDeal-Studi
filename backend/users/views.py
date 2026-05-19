from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
import logging

logger = logging.getLogger("autodeal")


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.info(f"Nouvel utilisateur inscrit — username: {user.username} — email: {user.email}")
        return Response({"message": "Compte cree avec succes"}, status=status.HTTP_201_CREATED)
    logger.warning(f"Echec inscription — erreurs: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Profil mis a jour — username: {request.user.username}")
        return Response(serializer.data)
    logger.error(f"Erreur mise a jour profil — username: {request.user.username} — erreurs: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]