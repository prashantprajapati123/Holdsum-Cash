import logging
from django.conf import settings

from plaid.errors import PlaidError

from .models import PLAID_STATES
from .views import Client


log = logging.getLogger('plaid')
INSUFFICIENT_FUNDS_CATEGORY_ID = '10007000'
MAXIMUM_INSUFFICENT_SCORE = -15
COUNT_INSUFFICIENT_TO_SCORE = {
    0: 15,
    1: 12,
    2: 9,
    3: -9,
    4: -12,
    5: -15,
}


def get_plaid_modifier(transactions):
    transactions = filter(lambda t: t['category_id'] == INSUFFICIENT_FUNDS_CATEGORY_ID, transactions)
    return COUNT_INSUFFICIENT_TO_SCORE.get(len(transactions), MAXIMUM_INSUFFICENT_SCORE)


def on_create_plaid(created=False, instance=None):
    if not created:
        return

    if not instance.borrower.plaid_access_token:
        instance.plaid_state = PLAID_STATES.no_token
        instance.save()

    client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET,
                    access_token=instance.borrower.plaid_access_token)
    try:
        transactions = client.connect_get().json()
        instance.plaid_score = get_plaid_modifier(transactions)
        instance.plaid_state = PLAID_STATES.success
        instance.save()
    except PlaidError as e:
        log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
        instance.plaid_state = PLAID_STATES.failed
        instance.save()
