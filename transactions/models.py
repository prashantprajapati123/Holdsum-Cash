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
    questionnaire = models.ForeignKey('transactions.Questionnaire', models.PROTECT)
    query = models.CharField(max_length=150)
    score = models.DecimalField(max_digits=4, decimal_places=2, help_text='e.g. 30 for 30%')
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.query


class Choice(models.Model):
    question = models.ForeignKey('transactions.Question', models.CASCADE, related_name='choices')
    option = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=4, decimal_places=2, help_text='0 - 5 for weighting the score.',
                                 validators=[MinValueValidator(D(0), MaxValueValidator(D(5)))])
    textbox = models.CharField(max_length=100, null=True, blank=True)
    is_alternative = models.BooleanField(default=False)

    def __str__(self):
        return self.option


class QuestionResponse(models.Model):
    request = models.ForeignKey('transactions.LoanRequest',
                                related_name='responses')
    choice = models.ForeignKey(Choice, models.PROTECT)
    textbox = models.TextField(blank=True, null=True)

    # these are saved from the choice/question
    score = models.DecimalField(max_digits=4, decimal_places=2)
    weight = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return 'Response to Question #{}'.format(self.choice.question_id)

    def save(self, **kwargs):
        if not self.score:
            self.score = self.choice.question.score
        if not self.weight:
            self.weight = self.choice.question.weight
        super().save(**kwargs)

    @property
    def total(self):
        return (self.weight / D(5)) * self.score if self.id else None


class LoanRequest(TimeStampedModel):
    borrower = models.ForeignKey('accounts.Profile', models.PROTECT)
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    state = models.CharField(max_length=30, choices=LOAN_STATES, default=LOAN_STATES.pending)

    def __str__(self):
        return '$%g request from %s' % (self.amount, self.borrower.user.username)

    @property
    def total_questions_score(self):
        return sum(r.total for r in self.responses.all())
