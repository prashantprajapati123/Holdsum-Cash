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
            {'fields': ('first_name', 'middle_initial', 'last_name', 'email', 'ssn', 'sex')}),
        ('Address',
            {'fields': ('address', 'city', 'state', 'zip_code')}),
        ('Income Data',
            {'fields':
                ('monthly_income', 'next_paydate', 'funds_source', 'pay_frequency')}),
        ('Documents',
            {'fields': ('license', 'paystubs')}),
    )
