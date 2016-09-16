from decimal import Decimal as D
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel


LOAN_STATES = Choices(
    ('rejected', 'rejected'),
    ('pending', 'pending'),
    ('awaiting_transfer', 'awaiting_transfer'),
    ('in_repayment', 'in_repayment'),
    ('paid_in_full', 'paid_in_full'),
)


class Questionnaire(models.Model):
    def __str__(self):
        return 'Main Questionnaire'


class Question(TimeStampedModel):
    questionnaire = models.ForeignKey(Questionnaire, models.PROTECT)
    query = models.CharField(max_length=150)
    score = models.DecimalField(max_digits=4, decimal_places=2, help_text='e.g. 30 for 30%')
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.query


class Choice(models.Model):
    question = models.ForeignKey(Question, models.CASCADE, related_name='choices')
    option = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=4, decimal_places=2, help_text='0 - 5 for weighting the score.',
                                 validators=[MinValueValidator(D(0), MaxValueValidator(D(5)))])
    textbox = models.CharField(max_length=100, null=True, blank=True)
    is_alternative = models.BooleanField(default=False)

    def __str__(self):
        return self.option
