from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import (
    generics, views, response, status, viewsets, permissions
)

from .serializers import RegisterSerializer, UserSerializer, RoleSerializer
from .models import Role
from permissions.permissions import IsAnonymousOrAdmin


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Вью-функция для регистрации."""
    
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousOrAdmin]
    authentication_classes = []


class UserView(views.APIView):
    """Вью-функция для пользователя."""
    
    element = 'user'

    def get_user(self, pk=None):
        user = self.request.user if pk is None else get_object_or_404(
            User, pk=pk, is_active=True
        )
        self.check_object_permissions(self.request, user)
        return user

    def get(self, request, pk=None):
        user = self.get_user(pk=pk)
        serializer = UserSerializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        user = self.get_user(pk=pk)
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        user = self.get_user(pk=pk)
        user.email = f'deleted_{self.email}'
        user.is_active = False
        user.save()

        return response.Response(
            {'message': 'Пользователь удален.'},
            status=status.HTTP_204_NO_CONTENT
        )


class RoleViewSet(viewsets.ModelViewSet):
    """Вью-функция для ролей."""

    element = 'roles'

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
