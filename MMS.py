
# Download the helper library from https://www.twilio.com/docs/python/install
import sys
from twilio.rest import Client
from SMS import Send_SMS
import ConfigValues

def Send_MMS(MMS_Message, MMS_Destination, URL):
    try:
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = ConfigValues.ReturnTwilioSID() 
        auth_token = ConfigValues.ReturnTwilioAuthToken() 
        client = Client(account_sid, auth_token)

        message = client.messages \
        .create(
                body=MMS_Message,
                from_= ConfigValues.ReturnTwilioSourcePhone(),
                #URL Must be publicly available and not require authentication
                media_url=[URL],
                to=MMS_Destination
            )

        print('MMS Sent Message ID: ' + message.sid)
    except:
        print("Oops!, MMS Error: ", sys.exc_info()[0], "occurred.")
        FailMessage = "MMS Failure, Fallback to SMS: " + MMS_Message
        Send_SMS(FailMessage, MMS_Destination)

