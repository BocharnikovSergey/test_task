from django.db import models

from .constants import MAX_LEN_BUSINESS_ELEMENT
from test_task.abstarct_models import TimeStampedModel
from users.models import Role


class BusinessElement(TimeStampedModel):
    """Модель для описания объектов к которым будет осуществляться доступ"""

    name = models.CharField(
        max_length=MAX_LEN_BUSINESS_ELEMENT, unique=True,
        verbose_name='Название объекта приложения')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Объект приложения'
        verbose_name_plural = 'Объекты приложения'
        ordering = ('name',)

    def __str__(self):
        return f'Объект приложения {self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, name={self.name})'


class PermissionRoleRule(TimeStampedModel):
    """Модель бизнес‑элементов системы - объектов."""

    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, verbose_name='Роль',
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        verbose_name='Объект приложения',
    )

    read_permission = models.BooleanField(
        default=False, verbose_name='Чтение объектов')
    read_all_permission = models.BooleanField(
        default=False, verbose_name='Чтение любых объектов'
    )

    create_permission = models.BooleanField(
        default=False, verbose_name='Создание объекта'
    )

    update_permission = models.BooleanField(
        default=False, verbose_name='Редактирование объекта'
    )
    update_all_permission = models.BooleanField(
        default=False, verbose_name='Редактирование любых объектов'
    )

    delete_permission = models.BooleanField(
        default=False, verbose_name='Удаление объекта'
    )
    delete_all_permission = models.BooleanField(
        default=False, verbose_name='Удаление любых объектов'
    )

    class Meta:
        verbose_name = 'Правило доступа роли'
        verbose_name_plural = 'Правила доступа ролей'
        ordering = ('role__name', 'element__name')
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'element'],
                name='unique_role_element'
            )
        ]

    def __str__(self):
        return f'Права {self.role.name} для {self.element.name}'

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'id={self.id}, '
            f'role={self.role.name}, '
            f'element={self.element.name}, '
            f'read={self.read_permission}, '
            f'read_all={self.read_all_permission}, '
            f'create={self.create_permission}, '
            f'update={self.update_permission}, '
            f'update_all={self.update_all_permission}, '
            f'delete={self.delete_permission}, '
            f'delete_all={self.delete_all_permission})'
        )
