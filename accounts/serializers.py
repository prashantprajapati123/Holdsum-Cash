from rest_framework import serializers

from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.Field(required=False)

    class Meta:
        model = Profile

    def create(self, validated_data):
        instance = super(UserProfileSerializer, self).create(validated_data)
        return instance


class LoginResponseSerializer(serializers.Serializer):

    def to_representation(self, obj):
        user = obj.user
        return {
            'key': obj.key,
            'has_profile': hasattr(user, 'profile'),
            'has_plaid': bool(hasattr(user, 'profile') and
                              user.profile.plaid_access_token)
        }
