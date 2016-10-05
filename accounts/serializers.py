from rest_framework import serializers

from .models import Employment


class EmploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employment


class LoginResponseSerializer(serializers.Serializer):

    def to_representation(self, obj):
        user = obj.user
        return {
            'key': obj.key,
            'has_profile': user.completed_profile,
            'has_plaid': bool(user.plaid_access_token)
        }
