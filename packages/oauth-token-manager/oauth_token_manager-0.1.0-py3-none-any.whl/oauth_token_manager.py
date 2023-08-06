import time

import requests


class OAuthTokenManager(object):
    def __init__(
        self,
        url,
        *,
        renew_pad_secs=60,
        **parameters
    ):
        self.url = url
        self.parameters = parameters
        self.renew_pad_secs = renew_pad_secs

        self._token = None
        self._exp = None

    def login(self):
        response = requests.post(self.url, data=self.parameters)
        response.raise_for_status()
        body = response.json()

        self._token = body['access_token']
        self._exp = time.time() + body['expires_in'] - self.renew_pad_secs

    @property
    def token(self):
        if (
            not self._token or
            not self._exp or
            time.time() > self._exp
        ):
            self.login()

        return self._token
