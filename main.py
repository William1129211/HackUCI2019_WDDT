"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/
Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.
"""

import argparse
import base64
import picamera
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC920f2da359f4d8b4af7b9478a0ef7ccc' 
auth_token = 'baa0db35e954d100ef1c8ab6daacafef'
client = Client(account_sid, auth_token)


def is_pet(pet_type, response):
    for analysis in response["responses"][0]["labelAnnotations"]:
        if analysis["description"].lower() == pet_type.lower():
            return True
    return False


def takephoto(count, camera):
    camera.capture('image' + str(count) + '.jpg')


def sendPhotoReceiveJSON(count, camera):
    takephoto(count, camera)

    """Run a label request on a single image"""
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image' + str(count) + '.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        
        print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.
        print("Dog?", "Yes" if is_pet("dog", response) else "No")

        if is_pet("dog", response):
            send_message(4088394928, 0)
        elif is_


def send_message(usr_num, condition):
    if condition == 0:
        body_text = "Dog is at home now, safe and happy :)"
    elif condition == 1:
        body_text = "A glutonous monstrousity is at your doorstep"
    elif condition == 2:
        body_text = "Someone is on your doorstep..."
        
    message = client.messages.create( \
        body=body_text,
        from_='+19495369863',
        to=usr_num)
        

def main():
    cntr = 1
    camera = picamera.PiCamera()
    while(1):
        sendPhotoReceiveJSON(cntr, camera)
        cntr += 1
        if cntr > 75
            cntr = 0

    

if __name__ == '__main__':

    main()
