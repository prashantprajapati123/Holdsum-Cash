from django.core.urlresolvers import reverse
from django.test import TestCase
import json

from model_mommy import mommy
from rest_framework.authtoken.models import Token


class UserAPITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.key = self.create_user()
        self.user = Token.objects.get(key=self.key).user
        mommy.make('accounts.Profile', user=self.user)

    def create_user(self):
        url = reverse('rest_register')
        data = dict(username='MrSmith', email='mrsmith@gmail.com',
                    password1='loantom3', password2='loantom3')
        return self.client.post(url, data).data['key']

    def auth_get(self, url, **kwargs):
        return self.client.get(url,
                               HTTP_AUTHORIZATION='Token %s' % self.key,
                               **kwargs)

    def auth_post(self, url, data, **kwargs):
        return self.client.post(url, json.dumps(data),
                                content_type='application/json',
                                HTTP_AUTHORIZATION='Token %s' % self.key,
                                **kwargs)
