import base64
import requests
from .auth import MpesaBase
import datetime


class MpesaExpress(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        print(self.authentication_token)

    def stk_push(self, business_shortcode=None, passcode=None, amount=None, callback_url=None, reference_code=None,
                 phone_number=None, description=None):
        """
        payload = {
          "BusinessShortCode": 174379,
          "Password": encoded,
          "Timestamp": time,
          "TransactionType": "CustomerPayBillOnline",
          "Amount": 10,
          "PartyA": 254701783003,
          "PartyB": 174379,
          "PhoneNumber": 254701783003,
          "CallBackURL": "https://1c55722e.ngrok.io/callback",
          "AccountReference": "13dbd6hg",
          "TransactionDesc": "Just a trial"
        }
        :return:
        {
            u'CustomerMessage': u'Success. Request accepted for processing',
            u'CheckoutRequestID': u'ws_CO_17102017141428735',
            u'ResponseDescription': u'Success. Request accepted for processing',
            u'MerchantRequestID': u'29127-1024378-1',
            u'ResponseCode': u'0'
        }
        """

        time = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ", "").replace(":", "")
        password = "{0}{1}{2}".format(str(business_shortcode), str(passcode), time)
        encoded = base64.b64encode(password)
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": encoded,
            "Timestamp": time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": int(phone_number),
            "PartyB": business_shortcode,
            "PhoneNumber": int(phone_number),
            "CallBackURL": callback_url,
            "AccountReference": reference_code,
            "TransactionDesc": description
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/stkpush/v1/processrequest")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

    def query(self, business_shortcode=None, checkout_request_id=None, passcode=None):
        """
        payload = {
                "BusinessShortCode": " " ,
                "Password": " ",
                "Timestamp": " ",
                "CheckoutRequestID": " "
        }
        :return:
        {
            u'MerchantRequestID': u'Success. Request accepted for processing',
            u'CheckoutRequestID': u'ws_CO_17102017141428735',
            u'ResponseCode': u'Success. Request accepted for processing',
            u'ResultDesc': u'29127-1024378-1',
            u'ResponseDescription': u'0',
            u'ResultCode': u'0'
        }
        """

        time = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ", "").replace(":", "")
        password = "{0}{1}{2}".format(str(business_shortcode), str(passcode), time)
        encoded = base64.b64encode(password)
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": encoded,
            "Timestamp": time,
            "CheckoutRequestID": checkout_request_id
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/stkpushquery/v1/query")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()
