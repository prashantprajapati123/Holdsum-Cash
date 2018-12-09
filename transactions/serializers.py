from rest_framework import serializers

from .models import LoanRequest, QuestionResponse
from accounts.serializers import BorrowerSerializer



class QuestionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionResponse
        fields = ('choice', 'textbox')


class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = serializers.HiddenField(default=serializers.CurrentUserDefault())
    responses = QuestionResponseSerializer(many=True)
    exclude = ('responses',)
    class Meta:
        model = LoanRequest
        fields = ('id', 'borrower', 'amount', 'repayment_date', 'responses')
        readonly_fields = ('id', 'borrower',)

    def create(self, data):
        responses = data.pop('responses')
        lr = LoanRequest.objects.create(**data)
        for response in responses:
            QuestionResponse.objects.create(
               request=lr,
               **response
           )
        return lr

class SearchLoanRequestSerializer(serializers.ModelSerializer):
    borrower = BorrowerSerializer(required=False)
    class Meta:
        model = LoanRequest
        fields = ('id', 'borrower', 'amount', 'repayment_date', 'state')
