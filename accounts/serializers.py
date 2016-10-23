from rest_framework import serializers

from .models import Employment, User, EMPLOYMENT_CHOICES


class EmploymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Employment


class UserSerializer(serializers.ModelSerializer):
    employment = EmploymentSerializer(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'middle_initial', 'ssn', 'sex',
                  'address', 'city', 'state', 'zip_code',
                  'monthly_income', 'next_paydate', 'funds_source', 'pay_frequency',
                  'license', 'paystubs', 'employment_status', 'employment',
                  'status',)
        read_only_fields = ('email', 'status')
        extra_kwargs = {'paystubs': {'write_only': True},
                        'license': {'write_only': True}}

    def update(self, instance, validated_data):
        employment = validated_data.pop('employment', None)
        instance = super().update(instance, validated_data)
        if instance.employment_status == EMPLOYMENT_CHOICES.employed:
            Employment.objects.update_or_create(
                defaults=employment,
                user=instance,
            )
        return instance


class LoginResponseSerializer(serializers.Serializer):

    def to_representation(self, obj):
        user = obj.user
        return {
            'key': obj.key,
            'has_profile': user.completed_profile,
            'has_plaid': bool(user.plaid_access_token)
        }
