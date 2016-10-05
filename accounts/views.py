import logging
from django.conf import settings

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from plaid.errors import PlaidError
from rest_auth.registration.views import SocialLoginView, LoginView as AuthLoginView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .plaidclient import Client
from .serializers import LoginResponseSerializer

log = logging.getLogger('plaid')


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    response_serializer = LoginResponseSerializer


class LoginView(AuthLoginView):
    response_serializer = LoginResponseSerializer


class PlaidTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET)
        try:
            client.exchange_token(request.data['token'])  # this populates client.access_token

            request.user.plaid_access_token = client.access_token
            request.user.plaid_public_token = request.data['token']
            request.user.save()

            client.upgrade('connect')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlaidError as e:
            log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
            return Response({'error': 'Something went wrong.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
