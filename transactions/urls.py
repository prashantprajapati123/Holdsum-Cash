from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import LoanRequestViewSet

router = DefaultRouter()
router.register(r'loan-request', LoanRequestViewSet, base_name='loan_request')

urlpatterns = [
    url('', include(router.urls)),
]
