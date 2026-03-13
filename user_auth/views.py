from rest_framework import views, response, status, permissions

from .serializers import LoginSerializer
from .jwt import create_jwt_token
from .constants import TOKEN_TYPE
from .models import DeactivatedToken


class LoginView(views.APIView):
    """Вью-функция для входа."""

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']

        token = create_jwt_token(user_id=user_id)
        DeactivatedToken.objects.filter(user_id=user_id).delete()
        return response.Response(
            {
                'token_type': TOKEN_TYPE,
                'access_token': token
            }, status=status.HTTP_200_OK
        )


class LogoutView(views.APIView):
    """Вью-функция для выхода."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        DeactivatedToken.objects.get_or_create(
            token=request.auth, user=request.user
        )
        return response.Response(
            {'detail': 'Вы вышли из системы'}, status=status.HTTP_200_OK
        )
