# Download the helper library from https://www.twilio.com/docs/python/install
import sys
from twilio.rest import Client
import ConfigValues

def Send_SMS(SMS_Message, SMS_Destination):
    try:
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = ConfigValues.ReturnTwilioSID() 
        auth_token = ConfigValues.ReturnTwilioAuthToken() 
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                 body=SMS_Message,
                 from_= ConfigValues.ReturnTwilioSourcePhone(),
                 to=SMS_Destination
             )

        print('SMS Sent Message ID: ' + message.sid)
    except:
        print("Oops! - SMS Error: ", sys.exc_info()[0], "occurred.")




