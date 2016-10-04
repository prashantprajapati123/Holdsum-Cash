from rest_framework import serializers

from .models import Employment, Profile, EMPLOYED


class EmploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employment


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    employment = EmploymentSerializer(required=False)

    class Meta:
        model = Profile
        fields = ('user', 'sex', 'employment_status',
                  'address', 'city', 'state', 'zip_code')

    def create(self, validated_data):
        employment = validated_data.pop('employment', None)
        profile = super().create(validated_data)
        if profile.employment_status in EMPLOYED:
            Employment.objects.create(
                profile=profile,
                **employment
            )
        return profile


class LoginResponseSerializer(serializers.Serializer):

    def to_representation(self, obj):
        user = obj.user
        return {
            'key': obj.key,
            'has_profile': hasattr(user, 'profile'),
            'has_plaid': bool(hasattr(user, 'profile') and
                              user.profile.plaid_access_token)
        }
