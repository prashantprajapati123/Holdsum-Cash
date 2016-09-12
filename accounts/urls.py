from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, base_name='profile')

urlpatterns = [
    url('', include(router.urls)),
]
