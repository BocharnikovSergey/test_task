from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserView, RoleViewSet

router = DefaultRouter()
router.register('roles', RoleViewSet, basename='role')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
    path('user/<int:pk>', UserView.as_view(), name='user_detail'),
    path('', include(router.urls))
]
