from rest_framework import serializers

from .models import Employment, User, EMPLOYMENT_CHOICES
from django.conf import settings
from rest_framework import status
from .plaidclient import Client
from plaid.errors import PlaidError




class EmploymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Employment


class UserSerializer(serializers.ModelSerializer):
    employment = EmploymentSerializer(required=False)

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email','username',
                  'middle_initial', 'ssn', 'sex',
                  'address', 'city', 'state', 'zip_code',
                  'monthly_income', 'plaid_public_token', 'next_paydate', 'funds_source', 'pay_frequency',
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

    def create(self, data):
        response = data.pop('employment')
        del response['user']
        user = User.objects.create(**data)
        Employment.objects.create(
               user=user,
               **response
           )
        try:
            self.set_plaid_token(user);

        except Exception as e:
            pass
        return user

    def set_plaid_token(self,user):
        client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET)
        try:
            client.exchange_token(user.plaid_public_token)  # this populates client.access_token
            user.plaid_access_token = client.access_token
            user.save()

            client.upgrade('connect')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlaidError as e:
            log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
            return Response({'error': 'Something went wrong.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginResponseSerializer(serializers.Serializer):

    def to_representation(self, obj):
        user = obj.user
        return {
            'key': obj.key,
            'has_profile': user.completed_profile,
            'has_plaid': bool(user.plaid_access_token)
        }
