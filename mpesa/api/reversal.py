import requests
from .auth import MpesaBase


class Reversal(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        print(self.authentication_token)

    def reverse(self, initiator=None, security_credential=None, command_id=None, transaction_id=None,
                 amount=None, receiver_party=None, receiver_identifier_type=None, queue_timeout_url=None,
                result_url=None, remarks=None, occassion=None):
        """
        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "TransactionID": transaction_id,
            "Amount": amount,
            "ReceiverParty": receiver_party,
            "ReceiverIdentifierType": receiver_identifier_type,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Remarks": remarks,
            "Occassion": occassion
        }
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
            "TransactionID": transaction_id,
            "Amount": amount,
            "ReceiverParty": receiver_party,
            "ReceiverIdentifierType": receiver_identifier_type,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Remarks": remarks,
            "Occassion": occassion
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/reversal/v1/request")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

