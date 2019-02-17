# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import time

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC920f2da359f4d8b4af7b9478a0ef7ccc'
auth_token = 'baa0db35e954d100ef1c8ab6daacafef'
client = Client(account_sid, auth_token)
usr_num = 0
twilioNum = '+19495369863'
detects = ['cat','dog','person']
#messages = client.messages.list(to='+19495369863')

#for record in messages:
    #print(record.from_)
def prompt_usr():
    '''Snatch program used client and modify dedicated usr_num
       assuming usr has last texted the program'''
    global twilioNum
    global client
    global usr_num
    messages = client.messages.list(to=twilioNum)
    usr_num = messages[0].from_
    client.messages.create(\
        body= """Hi! We are glad that you start using Pet Portal!
        Type:
        (1) if you have a dog
        (2) if you have a cat
        then follow by its name
        """,
        from_ = twilioNum,
        to=usr_num)

def ask_pets():
    '''modify  user has certain animals'''
    global twilioNum
    global detects
    global usr_num
    global client
    messages = client.messages.list(to=twilioNum)
    pet_code = (messages[0].body)[0]
    if pet_code not in ['1','2']:
        body_text = 'What do you have, an anteater? >:('
    else:
        if pet_code == '1':
            detects.remove('cat')
            pet_kind = 'dog'
        elif pet_code == '2':
            detects.remove('dog')
            pet_kind = 'cat'
        name = (messages[0].body)[1:].strip(' ')
        body_text = \
        '''Nice! {} is a good {} name! From now Pet Portal will notify you when {} comes home.'''\
        .format(name, pet_kind, name)
    client.messages.create(\
        body= body_text,
        from_ = twilioNum,
        to=usr_num)

prompt_usr()
time.sleep(15)
ask_pets()
    
    
