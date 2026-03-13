from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from test_task.abstarct_models import TimeStampedModel
from .constants import MAX_LEN_NAME, MAX_LEN_ROLE, DEFAULT_ROLE, ROLE_ADMIN


class ProjectUserManager(BaseUserManager):
    """Кастомный менеджер для модели ProjectUser."""

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Нужно указать email')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        if not getattr(user, 'role', None):
            user.role = Role.objects.get_or_create(name=DEFAULT_ROLE)[0]
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.objects.get_or_create(name=ROLE_ADMIN)[0]
        user.save(using=self._db)
        return user


class ProjectUser(AbstractBaseUser, TimeStampedModel):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    first_name = models.CharField(
        max_length=MAX_LEN_NAME, verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=MAX_LEN_NAME, verbose_name='Фамилия',
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Поле активности записи'
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        related_name='users'
    )

    objects = ProjectUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    @property
    def is_admin(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'Пользователь {self.first_name} {self.last_name}'

    def __repr__(self):
        return (
            f'{self.__class__.__name__} '
            f'(id={self.id}, email={self.email}, first_name={self.first_name},'
            f' last_name={self.last_name})'
        )


class Role(TimeStampedModel):
    """Модель роли в системе управления доступом."""

    name = models.CharField(
        max_length=MAX_LEN_ROLE, unique=True, verbose_name='Название роли'
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ('name',)

    def __str__(self):
        return f'Роль {self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, name={self.name})'
