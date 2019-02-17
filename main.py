"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/
Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.
"""

import argparse
import base64
import json
import picamera
import RPi.GPIO as GPIO
import time

from google.cloud import storage
from googleapiclient import discovery
from google.cloud import storage
from oauth2client.client import GoogleCredentials
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC920f2da359f4d8b4af7b9478a0ef7ccc' 
auth_token = 'baa0db35e954d100ef1c8ab6daacafef'
client = Client(account_sid, auth_token)

# For convenience
usr_num = 9097356894

"""
class Labels(Enum):
    DOG = 1;
    CAT = 2;
    PERSON = 3;
"""


def get_object(response):
    for analysis in response["responses"][0]["labelAnnotations"]:
        label_parsed = analysis["description"].lower()
        if label_parsed == "dog":
            return "dog"
        elif label_parsed == "cat":
            return "cat"
        elif label_parsed in ("hair", "face"):
            return "person"
    return "normal"


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
        
        #Debugging
        print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.

        url = cloudUpload(get_object(response), count)
        send_message(get_object(response), url)

def cloudUpload(condition, cnt):
    bucketName = 'hackuci-2019'
    sourceFileName = 'image' + str(cnt) + '.jpg'
    blobName = 'image' + str(cnt)              
 
    if (condition == "dog" or condition == "cat" or condition == "person"):
        storage_client = storage.Client();
        bucket = storage_client.get_bucket(bucketName)
        blob = bucket.blob(blobName)
        
        blob.upload_from_filename(sourceFileName)
        blob.make_public()

        return blob.public_url;


def send_message(condition, url):
    flag = False
    if condition == "dog":
        body_text = "Dog is home! " + url
        flag = True
    elif condition == "cat":
        body_text = "Cat is home! " + url
        flag = True
    elif condition == "person":
        body_text = "Someone came to the door! " + url
        flag = True
        
    if (flag):
        message = client.messages.create( \
            body=body_text,
            from_='+19495369863',
            to=usr_num)

def bucket_init():
    #Instantiates a client
    storage_client = storage.Client()
    
    bucket_name = 'hackuci-2019'
    
    #returns bucket
    return storage_client.create_bucket(bucket_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file_name)
    
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def open_door(object_id):
    if object_id == "dog" or object_id == "cat":
        GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(ledPin, GPIO.LOW)


def main():
    #Pin Definition:
    ledPin = 3

    #Pin Setup
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

    #Initial state for LED
    GPIO.output(ledPin, GPIO.LOW)

    cntr = 1
    camera = picamera.PiCamera()
    #bucket = bucket_init()

    try:
        while 1:
            sendPhotoReceiveJSON(cntr, camera)
            cntr += 1
            if cntr > 99:
                cntr = 0
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':

    main()
