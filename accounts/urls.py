from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, YodleeTokenView

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, base_name='profile')

urlpatterns = [
    url('yodlee_token', YodleeTokenView.as_view()),
    include('', router.urls)
]
