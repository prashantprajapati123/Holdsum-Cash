from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import LoanRequestViewSet
from .views import UserLoanRequestsViewSet, QuestionResponseViewSet, GetUserQuestionResponseList

router = DefaultRouter()
router.register(r'loan-request', LoanRequestViewSet, base_name='loan_request')
router.register(r'user-loan-request', UserLoanRequestsViewSet, base_name='user_loan_request')
router.register(r'save-questionnaire-choice', QuestionResponseViewSet, base_name='save_questionnaire_choice')
router.register(r'get-questionnaire-choice/(?P<request_id>\w+)', GetUserQuestionResponseList, base_name='get_questionnaire_choice')





urlpatterns = [
    url('', include(router.urls)),
]
