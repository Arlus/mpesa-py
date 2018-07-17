import requests
from requests.auth import HTTPBasicAuth


class MpesaBase:
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.token = None

    def authenticate(self):
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        authenticate_uri = "/oauth/v1/generate?grant_type=client_credentials"
        authenticate_url = "{0}{1}".format(base_safaricom_url, authenticate_uri)
        r = requests.get(authenticate_url,
                         auth=HTTPBasicAuth(self.app_key, self.app_secret))
        self.token = r.json()['access_token']
        return r.json()['access_token']
