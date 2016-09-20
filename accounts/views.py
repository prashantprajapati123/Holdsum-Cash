import logging
from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from plaid.errors import PlaidError
from rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .plaidclient import Client
from .serializers import UserProfileSerializer

log = logging.getLogger('plaid')


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class UserProfileViewSet(viewsets.ModelViewSet):
    base_name = 'profile'
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.profile

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@require_POST
def plaid_token(request):
    client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET)
    try:
        client.exchange_token(request.POST['token'])  # this populates client.access_token

        request.user.plaid_access_token = client.access_token
        request.user.plaid_public_token = request.POST['token']
        request.user.save()
        client.upgrade('connect')
        return HttpResponse(status=204)
    except PlaidError as e:
        log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
        return JsonResponse({'error': 'Something went wrong.'}, status=500)
