import requests as r
from os import environ
from twilio.rest import Client


# ----- TWILIO API -----
def send_sms(msg):
    account_sid = environ.get('account_sid')
    auth_token = environ.get('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=msg,
        from_="+18142584851",
        to="+5579988197789"
    )
    print('sms sent successfully')
