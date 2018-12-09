from rest_framework import serializers

from .models import Employment, User, EMPLOYMENT_CHOICES
from django.conf import settings
from rest_framework import status
from plaid.errors import PlaidError
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer


class EmploymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Employment


class UserSerializer(serializers.ModelSerializer):
    employment = EmploymentSerializer(required=False)

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email',
                  'middle_initial', 'ssn', 'sex',
                  'address', 'city', 'state', 'zip_code',
                  'monthly_income','next_paydate', 'plaid_public_token','funds_source', 'pay_frequency',
                  'license', 'paystubs', 'employment_status', 'employment',
                  'status','access_type',)
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
            'has_plaid': bool(user.plaid_access_token),
            'access_type': user.access_type
        }


class RegistrationSerializer(RegisterSerializer):
    access_type = serializers.CharField(required=True)
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'access_type':self.validated_data.get('access_type', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.access_type = self.cleaned_data['access_type']
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class BorrowerSerializer(serializers.ModelSerializer):
    employment = EmploymentSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'employment_status', 'employment','status',
                  'no_of_failed_transection','plaid_score', 'repayment_score')