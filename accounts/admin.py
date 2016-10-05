from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Employment, User


class EmploymentInline(admin.StackedInline):
    model = Employment


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [EmploymentInline]

    fieldsets = (
        (None,
            {'fields': ('username', 'password', 'status')}),
        ('Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'sex')}),
        ('Address',
            {'fields': ('address', 'city', 'state', 'zip_code'),
             'classes': ('collapse',)}),
        ('Documents',
            {'fields': ('license', 'paystubs'),
             'classes': ('collapse',)}),
    )
