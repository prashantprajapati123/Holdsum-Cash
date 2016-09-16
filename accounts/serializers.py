from rest_framework import serializers

from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.Field(required=False)

    class Meta:
        model = Profile

    def create(self, validated_data):
        instance = super(UserProfileSerializer, self).create(validated_data)
        return instance
