from decimal import Decimal as D
from django.core.exceptions import ValidationError
from django.test import TestCase

from model_mommy import mommy

from .models import Choice, LoanRequest, Question, QuestionResponse


class QuestionTests(TestCase):
    def test_display(self):
        question = mommy.make(Question, query='What time is it?')
        self.assertEqual(str(question), 'What time is it?')


class ChoiceTests(TestCase):
    def setUp(self):
        super().setUp()
        self.question = mommy.make(Question)

    def test_display(self):
        choice = mommy.make(Choice, option="3 o'clock")
        self.assertEqual(str(choice), "3 o'clock")

    def test_weight_min_max_validation(self):
        choice = mommy.prepare(Choice, weight=-2, question=self.question)
        self.assertRaises(ValidationError, choice.full_clean)

        choice = mommy.prepare(Choice, weight=8, question=self.question)
        self.assertRaises(ValidationError, choice.full_clean)

        choice = mommy.prepare(Choice, weight=4, question=self.question)
        choice.full_clean()


class QuestionResponseTests(TestCase):
    def test_display(self):
        choice = mommy.make(Choice, question=mommy.make(Question, id=7))
        qr = mommy.make(QuestionResponse, choice=choice)
        self.assertEqual(str(qr), 'Response to Question #7')

    def test_saving_sets_score_and_weight(self):
        choice = mommy.make(Choice, question=mommy.make(Question, score=D(25)), weight=D(4))
        qr = QuestionResponse(request=mommy.make(LoanRequest),
                              choice=choice, textbox=None)
        qr.save()

        qr.refresh_from_db()
        self.assertEqual(qr.weight, D(4))
        self.assertEqual(qr.score, D(25))

        self.assertEqual(qr.total, D(20))


class LoanRequestTests(TestCase):
    pass
