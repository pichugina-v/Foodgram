
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    re_path('', include(router.urls)),
    re_path('auth/', include('djoser.urls.authtoken')),
]
