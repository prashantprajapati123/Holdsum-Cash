from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import on_create_notify


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        User = self.get_model('User')
        post_save.connect(on_create_notify, User)
