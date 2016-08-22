from django.conf import settings
import requests

FINAPP_ID = 10003620  # Instant Account Verification
HEADERS = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}


class YodleeService:
    REST_URL = settings.YODLEE_REST_URL

    def _make_request(self, endpoint, data):
        url = self.REST_URL + endpoint
        r = requests.post(url, data, headers=HEADERS)
        r.raise_for_status()
        json = r.json()
        if 'Error' in json:
            raise requests.HTTPError(response=r)
        return json

    def coblogin(self):
        endpoint = '/authenticate/coblogin'
        data = {'cobrandLogin': settings.YODLEE_COBRAND_LOGIN,
                'cobrandPassword': settings.YODLEE_COBRAND_PASSWORD}
        return self._make_request(endpoint, data)['cobrandConversationCredentials']['sessionToken']

    def login(self, user, cob_session=None):
        endpoint = '/authenticate/login'
        if cob_session is None:
            cob_session = self.coblogin()

        data = {'cobSessionToken': cob_session,
                'login': user.username,
                'password': None}  # TODO
        return self._make_request(endpoint, data)['userContext']['conversationCredentials']['sessionToken']

    def register3(self, user, cob_session=None):
        endpoint = '/jsonsdk/UserRegistration/register3'
        if cob_session is None:
            cob_session = self.coblogin()

        data = {'cobSessionToken': cob_session,
                'userCredentials.loginName': user.username,
                'userCredentials.password': None,  # TODO
                'userCreddentials.objectInstanceType': 'com.yodlee.ext.login.PasswordCredentials',
                'userProfile.emailAddress': user.email}
        return self._make_request(endpoint, data)['userContext']['conversationCredentials']['sessionToken']

    def token(self, user_session, cob_session):
        endpoint = '/authenticator/token'
        data = {'cobSessionToken': cob_session,
                'ression': user_session,
                'finAppId': FINAPP_ID}
        infos = self._make_request(endpoint, data)['finappAuthenticationInfos']
        return infos['token'] if isinstance(infos, dict) else infos[0]['token']  # taken from the sample app

    def get_token(self, user):
        cob_session = self.coblogin()
        user_session = self.login(user, cob_session=cob_session)
        return self.token(user_session, cob_session)

yodlee = YodleeService()
