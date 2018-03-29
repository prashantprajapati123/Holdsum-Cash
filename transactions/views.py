from rest_framework.exceptions import PermissionDenied
from rest_framework import decorators, mixins, permissions, response, viewsets

from accounts.models import STATUS_CHOICES
from . import docusign
from .models import LoanRequest,QuestionResponse,Choice 
from .serializers import LoanRequestSerializer,QuestionResponseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from accounts.plaidclient import Client
from plaid.errors import PlaidError
from decimal import Decimal as D
from rest_framework.response import Response
from .signals import get_plaid_modifier
import datetime
import logging
log = logging.getLogger('plaid')







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
    



class GetUserScoreDetails(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        public_token = request.data['plaidToken']
        client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET, public_key=settings.PLAID_PUBLIC_KEY, environment='sandbox')
        total = 0 
        try:
            response = client.Item.public_token.exchange(public_token)
            request.user.plaid_access_token = response['access_token']
            request.user.plaid_public_token = public_token
            request.user.save()

            choice_resposne = request.data['responses']

            for ch in choice_resposne:
                try:
                    ch_obj = Choice.objects.get(id=ch['choice'])
                except:
                    pass
                if ch_obj:
                    score = (ch_obj.weight / D(5)) * ch_obj.question.score
                else:
                    score = 0
                total = total + score
            start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
            end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
            response = client.Transactions.get(request.user.plaid_access_token, start_date=start_date, end_date=end_date)
            transactions = response['transactions']
            user_plaid_score = get_plaid_modifier(transactions)

            return Response({'status':self.get_status(total,user_plaid_score)})
        except PlaidError as e:
            log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
            return Response({'error': 'Something went wrong.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def get_status(self,total,user_plaid_score):
        current_score = per = 0
        if user_plaid_score == 15:
            per = (total/100) * 15 
            current_score = per + total
        elif user_plaid_score == 12:
            per = (total/100) * 7.5
            current_score = total - per
        elif user_plaid_score == 9:
            per = (total/100) * 15
            current_score = total - per
        elif user_plaid_score == -9:
            per = (total/100) * 22.5
            current_score = total - per
        elif user_plaid_score == -12:
            per = (total/100) * 22.5
            current_score = total - per


        if current_score >= 60:
            return'approved'
        else:
            return 'declined'