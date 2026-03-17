from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Role
from .models import BusinessElement, PermissionRoleRule


User = get_user_model()


class BusinessElementSerializer(serializers.ModelSerializer):
    """Сериализатор для бизнес-объектов."""

    class Meta:
        model = BusinessElement
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class PermissionRoleRuleSerializer(serializers.ModelSerializer):
    """Сериализатор для прав на основе ролей."""

    role = serializers.SlugRelatedField(
        slug_field='name', queryset=Role.objects.all()
    )
    element = serializers.SlugRelatedField(
        slug_field='name', queryset=BusinessElement.objects.all()
    )

    class Meta:
        model = PermissionRoleRule
        fields = (
            'id', 'role', 'element',
            'read_permission', 'read_all_permission',
            'create_permission',
            'update_permission', 'update_all_permission',
            'delete_permission', 'delete_all_permission',
        )
        read_only_fields = ('id',)
