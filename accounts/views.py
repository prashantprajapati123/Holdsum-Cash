from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfileSerializer


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
