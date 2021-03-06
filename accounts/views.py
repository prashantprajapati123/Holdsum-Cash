import logging
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from plaid.errors import PlaidError
from rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import User, STATUS_CHOICES
from .plaidclient import Client


from .serializers import UserSerializer
from rest_framework import decorators, mixins, permissions, response, viewsets



log = logging.getLogger('plaid')


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class PlaidTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        public_token = request.data['token']
        client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET, public_key=settings.PLAID_PUBLIC_KEY, environment='sandbox')
        try:
            response = client.Item.public_token.exchange(public_token)
            request.user.plaid_access_token = response['access_token']
            request.user.plaid_public_token = public_token
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlaidError as e:
            log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
            return Response({'error': 'Something went wrong.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def approve(request, uid):
    user = User.objects.get(pk=uid)
    user.status = STATUS_CHOICES.approved
    user.save()
    user.notify('Your account has been approved!', 'Congratulations! Your Holdsum account has been approved!')
    messages.success(request, '%s Approved' % user.get_full_name())
    return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))


def deny(request, uid):
    user = User.objects.get(pk=uid)
    user.status = STATUS_CHOICES.denied
    user.save()
    user.notify('Your account has been denied', 'Sorry, your Holdsum account has been denied.')
    messages.success(request, '%s Denied' % user.get_full_name())
    return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))


