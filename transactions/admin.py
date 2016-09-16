from django.contrib import admin

import nested_admin

from .models import Choice, Question, Questionnaire


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 0


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 0


class QuestionnaireAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]

    def has_add_permission(self, request):
        return False


admin.site.register(Questionnaire, QuestionnaireAdmin)
