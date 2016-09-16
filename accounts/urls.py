from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import plaid_token, UserProfileViewSet

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, base_name='profile')

urlpatterns = [
    url('', include(router.urls)),
    url(r'plaid-token/$', plaid_token),
]
