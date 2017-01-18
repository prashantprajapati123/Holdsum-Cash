from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import LoanRequestViewSet
from .views import UserLoanRequestsViewSet

router = DefaultRouter()
router.register(r'loan-request', LoanRequestViewSet, base_name='loan_request')
router.register(r'user-loan-request', UserLoanRequestsViewSet, base_name='user_loan_request')

urlpatterns = [
    url('', include(router.urls)),
]
