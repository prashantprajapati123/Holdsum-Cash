from django.contrib import admin

import nested_admin
from solo.admin import SingletonModelAdmin

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
class QuestionnaireAdmin(nested_admin.NestedModelAdminMixin, SingletonModelAdmin):
    inlines = [QuestionInline]


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
        'repayment_date',
    )

    readonly_fields = (
        'borrower',
        'amount',
        'repayment_date',
        'get_state_display',
        'get_plaid_state_display',
        'plaid_score',
        'questions_score',
    )

    def get_state_display(self, obj):
        return obj.get_state_display()
    get_state_display.short_description = 'State'

    def get_plaid_state_display(self, obj):
        return obj.get_plaid_state_display()
    get_plaid_state_display.short_description = 'Plaid State'

    def has_add_permission(self, request):
        return False

    def questions_score(self, obj):
        return '%g / 100' % obj.total_questions_score
    questions_score.short_description = 'Questions Score'
