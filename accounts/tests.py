from django.core.urlresolvers import reverse
from django.test import TestCase
from unittest.mock import MagicMock, patch

from plaid.errors import PlaidError
from rest_framework.test import APIRequestFactory, force_authenticate

from .plaidclient import Client
from .views import PlaidTokenView


class PlaidTokenTests(TestCase):
    def setUp(self):
        self.url = reverse('exchange_plaid_token')
        self.factory = APIRequestFactory()

    def test_requires_authentication(self):
        request = self.factory.get(self.url)
        response = PlaidTokenView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_requires_post(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)

        response = PlaidTokenView.as_view()(request)
        self.assertEqual(response.status_code, 405)

    def test_returns_500_error_when_plaid_error_occurs(self):
        request = self.factory.post(self.url, {'token': 'abc'})
        force_authenticate(request, user=self.user)
        with patch.object(Client, 'exchange_token') as mock_token:
            mock_token.side_effect = PlaidError

            response = PlaidTokenView.as_view()(request)
            self.assertEqual(response.status_code, 500)

    def test_user_has_access_and_public_token_persisted(self):
        request = self.factory.post(self.url, {'token': 'abc'})
        force_authenticate(request, user=self.user)

        with patch('accounts.views.Client', autospec=True) as mock_client:

            client = MagicMock(autospec=True)
            client.access_token = 'tok123'
            mock_client.return_value = client

            response = PlaidTokenView.as_view()(request)
            self.assertEqual(response.status_code, 204)

            self.user.refresh_from_db()
            self.assertEqual(self.user.plaid_access_token, 'tok123')
            self.assertEqual(self.user.plaid_public_token, 'abc')
