from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ProjectUser, Role


@admin.register(ProjectUser)
class ProjectUserAdmin(UserAdmin):
    """Админ модель для пользователя."""

    model = ProjectUser
    filter_horizontal = ()

    list_display = (
        'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'role'
    )
    list_filter = ('is_active', 'is_staff', 'role')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'role')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Дата', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2',
                'role', 'is_staff', 'is_superuser'
            ),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Role)
