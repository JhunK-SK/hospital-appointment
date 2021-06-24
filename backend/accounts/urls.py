from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()
router.register('accounts', CustomUserViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls))
]
