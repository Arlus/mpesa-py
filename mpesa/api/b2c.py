import requests
from .auth import MpesaBase


class B2C(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        print(self.authentication_token)

    def transact(self, initiator_name=None, security_credential=None, command_id=None, amount=None, party_a=None, party_b=None, remarks=None,
                 queue_timeout_url=None, result_url=None, occassion=None):
        """
        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occassion": occassion

        :return:
        {

        }
        """

        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occassion": occassion
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/b2c/v1/paymentrequest")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

