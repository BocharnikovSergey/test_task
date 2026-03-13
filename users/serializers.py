from django.core import validators
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Role
from .constants import ROLE_ADMIN


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.filter(is_active=True),
            message='Пользователь с таким email уже существует'
        )]
    )
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password2': 'Пароли не совпадают.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    role = serializers.SlugRelatedField(
        slug_field='name', queryset=Role.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('id',)

    def validate_email(self, value):
        value = value.lower()
        validators.validate_email(value)
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(
            email=value, is_active=True
        ).exclude(id=user_id).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return value

    def validate_role(self, value):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if (
            not user
            or not user.is_admin
            or not (user.role and user.role.name == ROLE_ADMIN)
        ):
            raise serializers.ValidationError(
                'Изменять роль может только администратор'
            )
        return value


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для ролей."""

    class Meta:
        model = Role
        fields = ('id', 'name', 'descriptions')
        read_only_fields = ('id',)
