import requests
from .auth import MpesaBase


class Balance(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        print(self.authentication_token)

    def get_balance(self, initiator=None, security_credential=None, command_id=None, party_a=None, identifier_type=None,
                    remarks=None, queue_timeout_url=None,result_url=None):
        """
        payload = {
          "Initiator": initiator,
          "SecurityCredential": security_credential,
          "CommandID": command_id,
          "PartyA": party_a
          "IdentifierType": identifier_type,
          "Remarks": remarks
          "QueueTimeOutURL": queue_timeout_url
          "ResultURL": result_url

        :return:
        {
            OriginatorConverstionID
            ConversationID
            ResponseDescription
        }
        """

        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/accountbalance/v1/query")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

