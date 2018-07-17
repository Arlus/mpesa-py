import base64
import requests
from .auth import MpesaBase
import datetime


class TransactionStatus(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        print(self.authentication_token)

    def check_transaction_status(self, party_a=None, identifier_type=None, remarks=None, initiator=None, passcode=None,
                                 result_url=None, queue_timeout_url=None, transaction_id=None,
                                 occassion=None, shortcode=None):
        """

        SAFARICOM PAYLOAD:
        {
          "CommandID": "TransactionStatusQuery",
          "PartyA": , # MSISDN or shortcode
          "IdentifierType": , 1-MSISDN. 2-Till Number, 3-Shortcode
          "Remarks": "",
          "Initiator": ,
          "SecurityCredential": "",
          "QueueTimeOutURL": encoded,
          "ResultURL": time,
          "TransactionID": checkout_request_id,
          "Occasion": ""
        }
        RESPONSE:
        1. LINE BUSY
        {
            u'ResultDesc': u'[STK_CB - ]Unable to lock subscriber, a transaction is already in process for the current subscriber',
            u'CheckoutRequestID': u'ws_CO_17102017143731981',
            u'ResponseDescription': u'The service request has been accepted successsfully',
            u'MerchantRequestID': u'29126-1025953-1',
            u'ResponseCode': u'0',
            u'ResultCode': u'1001'
        }
        2. SUCCESS
        {
            u'ResultDesc': u'The service request is processed successfully.',
            u'CheckoutRequestID': u'ws_CO_25102017143700816',
            u'ResponseDescription': u'The service request has been accepted successsfully',
            u'MerchantRequestID': u'32595-6738-1',
            u'ResponseCode': u'0',
            u'ResultCode': u'0'
        }
        3. CANCELLED BY USER
        {
            u'ResultDesc': u'[STK_CB - ]Request cancelled by user',
            u'CheckoutRequestID': u'ws_CO_25102017152900284',
            u'ResponseDescription': u'The service request has been accepted successsfully',
            u'MerchantRequestID': u'32593-14401-1',
            u'ResponseCode': u'0',
            u'ResultCode': u'1032'
        }

        4. INSUFFICIENT BALANCE
        {
            u'ResultDesc': u'[MpesaCB - ]The balance is insufficient for the transaction.',
            u'CheckoutRequestID': u'ws_CO_25102017153023394',
            u'ResponseDescription': u'The service request has been accepted successsfully',
            u'MerchantRequestID': u'16761-2730-1',
            u'ResponseCode': u'0',
            u'ResultCode': u'1'
        }
        :return: {"email": "", "status": ""}
        - Status can be "okay", "failed" or "unknown".
        """

        time = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ", "").replace(":", "")
        password = "{0}{1}{2}".format(str(shortcode), str(passcode), time)
        encoded = base64.b64encode(password)
        payload = {
            "CommandID": "TransactionStatusQuery",
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "Initiator": initiator,
            "SecurityCredential": encoded,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "TransactionID": transaction_id,
            "Occasion": occassion
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/stkpushquery/v1/query")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()
