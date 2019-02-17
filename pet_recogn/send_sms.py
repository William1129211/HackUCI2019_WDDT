# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC920f2da359f4d8b4af7b9478a0ef7ccc' 
auth_token = 'baa0db35e954d100ef1c8ab6daacafef'
client = Client(account_sid, auth_token)

#usr_num = input("Enter your phone number")
usr_num = '+19493003552'

def send_message(usr_num:str, condition:int):
    if condition ==: 0:
        body_text = "Dog is at home now, safe and happy :)"
    elif condition == 1:
        body_text = "A glutonous monstrousity is at your doorstep"
    elif condition == 2;
        body_text = "Someone is on your doorstep..."
        
    message = client.messages.create( \
        body=body_text,
        from_='+19495369863',
        to=usr_num)

print(message.sid)

