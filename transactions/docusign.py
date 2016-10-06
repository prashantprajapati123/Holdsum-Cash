from decimal import Decimal as D
from django.conf import settings
import json

import requests

HEADERS = {
    'X-DocuSign-Authentication': json.dumps({
        'Username': settings.DOCUSIGN_USERNAME,
        'Password': settings.DOCUSIGN_PASSWORD,
        'IntegratorKey': settings.DOCUSIGN_INTEGRATOR_KEY
    })
}

ENDPOINT = settings.DOCUSIGN_ENDPOINT
TEMPLATE_ID = settings.DOCUSIGN_TEMPLATE_ID


def login():
    r = requests.get(ENDPOINT, headers=HEADERS)
    r.raise_for_status()
    return r.json()['loginAccounts'][0]


def make_envelope(lr, account):
    user = lr.borrower
    env = {
        'accountId': account['accountId'],
        'templateId': TEMPLATE_ID,
        'templateRoles': [{
            'roleName': 'Signer',
            'clientUserId': user.pk,
            'email': user.email,
            'name': user.get_full_name(),
            'tabs': {
                'textTabs': []
            },
        }],
        'status': 'sent',
    }
    add_tab = lambda t: env['templateRoles'][0]['tabs']['textTabs'].append(t)
    make_tab = lambda label, value: {'tabLabel': label, 'value': value}

    add_tab(make_tab('first_name', user.first_name))
    add_tab(make_tab('middle_initial', user.middle_initial))
    add_tab(make_tab('last_name', user.last_name))
    add_tab(make_tab('address', user.address))
    add_tab(make_tab('city', user.city))
    add_tab(make_tab('state', user.state))
    add_tab(make_tab('zip', user.zip_code))
    add_tab(make_tab('ssn', user.ssn))
    add_tab(make_tab('transaction_number', lr.pk))
    add_tab(make_tab('\\*repayment_date', lr.repayment_date.strftime('%m/%d/%Y')))
    add_tab(make_tab('\\*amount', '$%s' % (lr.amount.quantize(D('.01')))))
    add_tab(make_tab('\\*transaction_fee', '$%s' % (lr.fee.quantize(D('.01')))))
    add_tab(make_tab('\\*payback_amount', '$%s' % (lr.amount + lr.fee + D('2')).quantize(D('.01'))))

    r = requests.post(account['baseUrl'] + '/envelopes', json=env, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def do_recipient(lr, account, envelopeURI):
    user = lr.borrower
    url = account['baseUrl'] + envelopeURI + '/views/recipient'
    data = {
        'authenticationMethod': 'Password',
        'clientUserId': user.pk,
        'email': user.email,
        'userName': user.get_full_name(),
        'returnUrl': 'holdsum://handleDocuSign',
    }
    r = requests.post(url, json=data, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_signing_url(lr):
    account = login()
    envelope = make_envelope(lr, account)
    return do_recipient(lr, account, envelope['uri'])
