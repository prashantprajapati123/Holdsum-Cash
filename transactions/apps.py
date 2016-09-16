from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import on_create_plaid


class TransactionsConfig(AppConfig):
    name = 'transactions'

    def ready(self):
        LoanRequest = self.get_model('LoanRequest')
        post_save.connect(on_create_plaid, LoanRequest)
