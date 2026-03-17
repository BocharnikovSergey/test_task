from django.db import models
from django.contrib.auth import get_user_model

from test_task.abstarct_models import TimeStampedModel

User = get_user_model()


class DeactivatedToken(TimeStampedModel):
    """Модель в которой хранятся токены при выходи из системы."""

    token = models.TextField(unique=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )

    def __str__(self):
        return f'token={self.token}'

    def __repr__(self):
        return (
            f'{self.__class__.__name__} '
            f'(user_id={self.user}, token={self.token})'
        )
