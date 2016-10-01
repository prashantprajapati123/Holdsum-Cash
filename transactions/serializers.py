from rest_framework import serializers

from .models import LoanRequest, QuestionResponse


class QuestionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionResponse
        fields = ('choice', 'textbox')


class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = serializers.HiddenField(default=serializers.CurrentUserDefault())
    responses = QuestionResponseSerializer(many=True)

    class Meta:
        model = LoanRequest
        fields = ('borrower', 'amount', 'repayment_date', 'responses')

    def create(self, data):
        responses = data.pop('responses')
        lr = LoanRequest.objects.create(data)
        for response in responses:
            QuestionResponse.objects.create(
                request=lr,
                **response
            )
        return lr
