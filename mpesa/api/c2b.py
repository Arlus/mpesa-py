import requests
from .auth import MpesaBase


class C2B(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        import sys

        sys.stderr.write(self.authentication_token)

    def register(self, shortcode=None, response_type=None, confirmation_url=None, validation_url=None):
        """
        payload = {
          "ShortCode": 174379, # The short code of the organization.
          "ResponseType": response_type, # Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction
          "ConfirmationURL": confirmation_url, # Confirmation URL for the client
          "ValidationURL": validation_url # Validation URL for the client

        :return:
        {
            "OriginatorConverstionID": ,
            "ConversationID": ,
            "ResponseDescription: ,
        }
        """

        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/registerurl")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

    def simulate(self, shortcode=None, command_id=None, amount=None, msisdn=None, bill_ref_number=None):
        """
        payload = {
          "ShortCode": 174379, # Short Code receiving the amount being transacted
          "CommandID": command_id, # Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline
          "Amount": amount, # The amount being transacted
          "Msisdn": 254XXXXXXXXX, # Phone number (msisdn) initiating the transaction MSISDN(12 digits)
          "BillRefNumber": Bill Reference Number, # Optional
        }
        :return:
        {
            "OriginatorConverstionID": ,
            "ConversationID": ,
            "ResponseDescription: ,
        }
        """

        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/simulate")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()
