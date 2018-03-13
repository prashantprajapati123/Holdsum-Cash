import logging
from django.conf import settings
import datetime


from plaid.errors import PlaidError

from accounts.plaidclient import Client
from .constants import PLAID_STATES, MAXIMUM_INSUFFICENT_SCORE


log = logging.getLogger('plaid')
INSUFFICIENT_FUNDS_CATEGORY_ID = '10007000'
COUNT_INSUFFICIENT_TO_SCORE = {
    0: 15,
    1: 12,
    2: 9,
    3: -9,
    4: -12,
    5: -15,
}


def get_plaid_modifier(transactions):
    transactions = filter(lambda t: 'category_id' in t and t['category_id'] == INSUFFICIENT_FUNDS_CATEGORY_ID,
                          transactions)
    return COUNT_INSUFFICIENT_TO_SCORE.get(len(list(transactions)), MAXIMUM_INSUFFICENT_SCORE)


def on_create_plaid(created=False, instance=None, **kwargs):
    if not created:
        return

    if not instance.borrower.plaid_access_token:
        instance.plaid_state = PLAID_STATES.no_token
        instance.save()
        return
    client = Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET, public_key=settings.PLAID_PUBLIC_KEY, environment='sandbox')

    try:
        start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
        response = client.Transactions.get(instance.borrower.plaid_access_token, start_date=start_date, end_date=end_date)
        transactions = response['transactions']
        instance.plaid_score = get_plaid_modifier(transactions)
        instance.plaid_state = PLAID_STATES.success
        instance.save()
    except PlaidError as e:
        log.warning('Issue with Plaid! Code %s, Message: %s', e.code, e.message)
        instance.plaid_state = PLAID_STATES.failed
        instance.save()
