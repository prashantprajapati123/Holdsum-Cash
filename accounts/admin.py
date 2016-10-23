from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Employment, User
from .views import approve, deny


class EmploymentInline(admin.StackedInline):
    model = Employment


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [EmploymentInline]
    list_display = DjangoUserAdmin.list_display + ('status',)
    readonly_fields = ('status',)
    list_filter = ('status',)

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

    def get_urls(self):
        return [
            url(
                r'^(.+)/approve/$',
                self.admin_site.admin_view(approve),
                name='approve',
            ),
            url(
                r'^(.+)/deny/$',
                self.admin_site.admin_view(deny),
                name='deny',
            ),
        ] + super().get_urls()
