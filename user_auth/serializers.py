from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа."""

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email, is_active=True).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError('Неверный email или пароль')
        attrs['user_id'] = user.id
        return attrs
