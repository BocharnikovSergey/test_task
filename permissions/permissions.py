from rest_framework.permissions import BasePermission

from .models import PermissionRoleRule
from users.constants import ROLE_ADMIN


class IsAdmin(BasePermission):
    """Права доступа для администратора."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated
            and (user.is_admin or (user.role and user.role.name == ROLE_ADMIN))
        )


class IsAnonymousOrAdmin(IsAdmin):
    """Права доступа для анонимного пользователя или администратора."""

    def has_permission(self, request, view):

        return (
            (request.user and not request.user.is_authenticated)
            or super().has_permission(request, view)
        )


class ProjectPermission(BasePermission):
    """Права для пользователей для проекта."""

    METHOD_PERMISSION = {
        'GET': ('read_permission', 'read_all_permission'),
        'POST': ('create_permission',),
        'PUT': ('update_permission', 'update_all_permission'),
        'PATCH': ('update_permission', 'update_all_permission'),
        'DELETE': ('delete_permission', 'delete_all_permission'),
    }

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            element_name = getattr(view, 'element', None)
            rule = PermissionRoleRule.objects.filter(
                role=request.user.role, element__name=element_name
            ).first()
            view.rule = rule
            permissions = self.METHOD_PERMISSION.get(request.method)

            return request.user.is_admin or (
                rule and permissions and any(
                    getattr(
                        rule, permission, False
                    ) for permission in permissions
                )
            )
        return False

    def has_object_permission(self, request, view, obj):
        rule = getattr(view, 'rule', None)
        permissions = self.METHOD_PERMISSION.get(request.method)
        user = getattr(obj, 'user', obj)
        return (
            request.user.is_admin
            or request.method == 'POST'
            or (len(permissions) > 1 and getattr(rule, permissions[1]))
            or (getattr(rule, permissions[0], False) and user == request.user)
        )
