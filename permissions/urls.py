from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BusinessElementViewSet, PermissionRoleRuleViewSet


router = DefaultRouter()
router.register('elements/', BusinessElementViewSet, basename='element')
router.register(
    'permissions/', PermissionRoleRuleViewSet, basename='permission'
)

urlpatterns = [
    path('', include(router.urls))
]
