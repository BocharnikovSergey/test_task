from rest_framework import viewsets

from .serializers import (
    BusinessElementSerializer, PermissionRoleRuleSerializer,
)
from .models import BusinessElement, PermissionRoleRule


class BusinessElementViewSet(viewsets.ModelViewSet):
    """Вью-функция для элементов системы."""

    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    element = 'elements'


class PermissionRoleRuleViewSet(viewsets.ModelViewSet):
    """Вью-функция для прав доступа на основе ролей."""

    queryset = PermissionRoleRule.objects.all()
    serializer_class = PermissionRoleRuleSerializer
    element = 'permissions'
