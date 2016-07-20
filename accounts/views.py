from django.shortcuts import render
from django.http import HttpResponse

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .models import Profile, Employment
from .serializers import EmploymentSerializer, UserProfileSerializer

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class UserProfileViewSet(viewsets.ModelViewSet):
    base_name = 'profile'
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        objects = []
        if self.request.user.is_authenticated():
            objects = Profile.objects.filter(user = self.request.user)

        return objects
    
    def perform_create(self, serializer):
        print 'serializer_data', serializer
        serializer.save(user=self.request.user)