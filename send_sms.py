# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC920f2da359f4d8b4af7b9478a0ef7ccc' 
auth_token = 'baa0db35e954d100ef1c8ab6daacafef'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+19495369863',
                     to='+19493003552'
                 )

print(message.sid)

