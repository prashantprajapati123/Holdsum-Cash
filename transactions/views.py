from rest_framework.exceptions import PermissionDenied
from rest_framework import decorators, mixins, permissions, response, viewsets

from accounts.models import STATUS_CHOICES
from . import docusign
from .models import LoanRequest,QuestionResponse,Choice 
from .serializers import ( 
    LoanRequestSerializer,
    QuestionResponseSerializer,
    SearchLoanRequestSerializer,
    )
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
from accounts.models import User
from .constants import LOAN_STATES


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

    def get_queryset(self):
        """
        This view should return a list of all the LoanRequest
        for the currently authenticated user.
        """
        user = self.request.user
        return LoanRequest.objects.filter(borrower=user)

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
        try:
            public_token = request.data['plaidToken']
        except:
            public_token = None
        client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET, public_key=settings.PLAID_PUBLIC_KEY, environment='sandbox')
        total = 0 
        insf_trans = {15:0,12:1,9:2,-9:3,-12:4,-15:5}
        try:
            if public_token: 
                response = client.Item.public_token.exchange(public_token)
                request.user.plaid_access_token = response['access_token']
                request.user.plaid_public_token = public_token
                request.user.save()


            if 'responses' in request.data.keys():
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
            if public_token:
                response = client.Transactions.get(request.user.plaid_access_token, start_date=start_date, end_date=end_date)
                transactions = response['transactions']
                user_plaid_score = get_plaid_modifier(transactions)
                request.user.no_of_failed_transection = insf_trans[user_plaid_score]
                request.user.plaid_score = user_plaid_score 
            else:
                user_plaid_score = request.user.plaid_score

            request.user.questionnaire_score = total
            request.user.repayment_score = (user_plaid_score + total)
            request.user.save()
            return Response({'status':self.get_status(total,user_plaid_score)})
        except PlaidError as e:
            log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
            return Response({'error': 'Something went wrong.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def get_status(self,total,user_plaid_score):
        if total == 0:
            total = 100

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
            self.request.user.status = 'approved'
            self.request.user.save()
            return'approved'
        else:
            self.request.user.status = 'denied'
            self.request.user.save()
            return 'declined'


class LoanRequestFilterViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A viewset for filtering Loan Requests.
    """
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = SearchLoanRequestSerializer
    queryset = LoanRequest.objects.all()
    
    def get_queryset(self):
        data = self.request.GET
        query_set = LoanRequest.objects.filter(state=LOAN_STATES.pending)
        if data.get('amount'):
            query_set= query_set.filter(amount=data['amount'])

        if data.get('state'):
            query_set= query_set.filter(state=data['state'])

        if data.get('date'):
            date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
            query_set= query_set.filter(repayment_date=date)
        """
        This view should return a list of all the LoanRequest
        for the currently authenticated user.
        """
        return query_set