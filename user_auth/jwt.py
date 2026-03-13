
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

from .constants import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_jwt_token(user_id):
    """Создание JWT токена."""
    payload = {
        'user_id': user_id,
        'exp': (
            datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        ),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token):
    """Декодирование JWT токине"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(payload, datetime.now(timezone.utc) + timedelta(seconds=1))
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
