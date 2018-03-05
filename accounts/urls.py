from django.conf.urls import url

from .views import PlaidTokenView


urlpatterns = [
    url(r'plaid-token/$', PlaidTokenView.as_view(), name='exchange_plaid_token'),
]
