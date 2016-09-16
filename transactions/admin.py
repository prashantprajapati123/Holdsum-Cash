from decimal import Decimal as D
from django.contrib import admin

import nested_admin

from .models import Choice, LoanRequest, Question, Questionnaire,\
    QuestionResponse


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 0


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 0


@admin.register(Questionnaire)
class QuestionnaireAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]

    def has_add_permission(self, request):
        return False


class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    fields = ('question', 'answer', 'textbox', 'weight', 'score', 'total',)
    readonly_fields = ('question', 'answer', 'textbox', 'weight', 'score', 'total')

    def question(self, obj):
        return obj.choice.question.query

    def answer(self, obj):
        return obj.choice.option

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    inlines = [QuestionResponseInline]
    list_display = (
        'borrower',
        'amount',
        'state',
    )

    readonly_fields = (
        'borrower',
        'amount',
        'state',
        'plaid_state',
        'plaid_score',
        'questions_score',
    )

    def has_add_permission(self, request):
        return False

    def questions_score(self, obj):
        return '%g / 100' % obj.total_questions_score
    questions_score.short_description = 'Questions Score'
