import requests
from .auth import MpesaBase


class B2B(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()
        print(self.authentication_token)

    def transact(self, initiator=None, security_credential=None, command_id=None, sender_identifier_type=None,
                 receiver_identifier_type=None, amount=None, party_a=None, party_b=None, remarks=None,
                 account_reference=None, queue_timeout_url=None, result_url=None):
        """
        payload = {
          "Initiator": initiator, # Username used to authenticate the transaction
          "SecurityCredential": security_credential,  # Generate from developer portal
          "CommandID": command_id, # Options:   BusinessPayBill
                                                BusinessBuyGoods
                                                DisburseFundsToBusiness
                                                BusinessToBusinessTransfer
                                                BusinessTransferFromMMFToUtility
                                                BusinessTransferFromUtilityToMMF
                                                MerchantToMerchantTransfer
                                                MerchantTransferFromMerchantToWorking
                                                MerchantServicesMMFAccountTransfer
                                                AgencyFloatAdvance
          "SenderIdentifierType": sender_identifier_type,  # 2 for Till Number, 4 for organization shortcode
          "RecieverIdentifierType": RecieverIdentifierType  # 2 for Till Number, 4 for organization shortcode
          "Amount": amount
          "PartyA": party_a  # Sender shortcode
          "PartyB": party_b  # Receiver shortcode
          "Remarks": remarks  # Comments that are sent along with the transaction(maximum 100 characters)
          "AccountReference": account_reference # Use if doing paybill to banks etc.
          "QueueTimeOutURL": queue_timeout_url  # The url that handles information of timed out transactions.
          "ResultURL": result_url # The url that receives results from M-Pesa api call.

        :return:
        {
            "OriginatorConverstionID": The unique request ID for tracking a transaction
            "ConversationID": The unique request ID returned by mpesa for each request made
            "ResponseDescription": Response Description message
        }
        """

        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "SenderIdentifierType": sender_identifier_type,
            "RecieverIdentifierType": receiver_identifier_type,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "AccountReference": account_reference,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url
        }
        headers = {'Authorization': 'Bearer {0}'.format(self.authentication_token), 'Content-Type': "application/json"}
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/b2b/v1/paymentrequest")
        r = requests.post(saf_url, headers=headers, json=payload)
        return r.json()

