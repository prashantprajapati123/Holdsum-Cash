from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import PlaidTokenView, UserProfileViewSet

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, base_name='profile')

urlpatterns = [
    url('', include(router.urls)),
    url(r'plaid-token/$', PlaidTokenView.as_view(), name='exchange_plaid_token'),
]
