from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

from .jwt import decode_jwt_token
from .models import DeactivatedToken


User = get_user_model()


class JWTAuth(authentication.BaseAuthentication):
    """Кастомная аутенцификация для проекта."""

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split()[1]
        user_id = decode_jwt_token(token=token)
        if (
            not user_id
            or DeactivatedToken.objects.filter(
                token=token, user_id=user_id
            ).exists()
        ):
            raise exceptions.AuthenticationFailed(
                'Неверный или просроченный токен'
            )
        user = User.objects.filter(id=user_id, is_active=True).first()
        if not user:
            raise exceptions.AuthenticationFailed('Пользователь не найден')
        return (user, token)
