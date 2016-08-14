from rest_framework import serializers

from .models import Profile, Employment


class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = ("employer", "role", "address", "city", "state", "zipCode",
                  "monthly_income", "income_frequency", "next_pay_date", )


class UserProfileSerializer(serializers.ModelSerializer):
    employment = EmploymentSerializer(required=False)
    user = serializers.Field(required=False)

    class Meta:
        model = Profile

    def create(self, validated_data):
        instance = super(UserProfileSerializer, self).create(validated_data)
        return instance
