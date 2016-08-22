from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from requests import HTTPError
from rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfileSerializer
from .yodlee import yodlee


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


class YodleeTokenView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            token = yodlee.get_token(request.user)
            return Response({'token': token})
        except HTTPError as e:
            pass
