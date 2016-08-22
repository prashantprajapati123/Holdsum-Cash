from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import on_create_link_yodlee


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        Profile = self.get_model('Profile')
        post_save.connect(on_create_link_yodlee, Profile)
