from rest_framework.exceptions import PermissionDenied
from rest_framework import decorators, mixins, permissions, response, viewsets

from accounts.models import STATUS_CHOICES
from . import docusign
from .models import LoanRequest,QuestionResponse 
from .serializers import LoanRequestSerializer,QuestionResponseSerializer


class LoanRequestViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A viewset for creating Loan Requests.
    """
#    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanRequestSerializer
    queryset = LoanRequest.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.status != STATUS_CHOICES.approved:
            raise PermissionDenied
        return super().create(request, *args, **kwargs)
    
    
    @decorators.detail_route(methods=['POST'], url_path='signing-url')
    def signing_url(self, request, pk=None):
        lr = self.get_object()
        url = docusign.get_signing_url(lr)
        return response.Response(url)

class UserLoanRequestsViewSet(viewsets.ViewSet):
    queryset = LoanRequest.objects.select_related('borrower').all()
    serializer_class = LoanRequestSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(borrower__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class QuestionResponseViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A viewset for creating Loan Requests.
    """
#    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionResponseSerializer
    queryset = QuestionResponse.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class GetUserQuestionResponseViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A viewset for creating Loan Requests.
    """
#    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionResponseSerializer
    queryset = QuestionResponse.objects.all()

    def post(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)

class GetUserQuestionResponseList(mixins.ListModelMixin,mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = QuestionResponseSerializer

    def get_queryset(self):
        """
        This view should return a list of all models by
        the maker passed in the URL
        """
        request_id = self.kwargs['request_id']
        return QuestionResponse.objects.filter(request=request_id)
    