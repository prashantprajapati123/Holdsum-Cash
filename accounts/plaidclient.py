from django.conf import settings

from plaid import Client

Client.config({'url': settings.PLAID_ENDPOINT})
