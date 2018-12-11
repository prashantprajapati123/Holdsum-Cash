from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import LoanRequestViewSet, LoanRequestFilterViewSets, FailedTransectionsList
from .views import UserLoanRequestsViewSet, QuestionResponseViewSet, GetUserQuestionResponseList,GetUserScoreDetails

router = DefaultRouter()
router.register(r'loan-request', LoanRequestViewSet, base_name='loan_request')
router.register(r'user-loan-request', UserLoanRequestsViewSet, base_name='user_loan_request')
router.register(r'save-questionnaire-choice', QuestionResponseViewSet, base_name='save_questionnaire_choice')
router.register(r'get-questionnaire-choice/(?P<request_id>\w+)', GetUserQuestionResponseList, base_name='get_questionnaire_choice')
router.register(r'get-user-score', GetUserScoreDetails, base_name='get_user_score')
router.register(r'search-loan-request', LoanRequestFilterViewSets, base_name='search_loan_request')







urlpatterns = [
    url('', include(router.urls)),
    url(r'get-user-score/$', GetUserScoreDetails.as_view(), name='get_user_score'),
    url(r'get-failed-transections/$', FailedTransectionsList.as_view(), name='get_failed_transection'),


]
