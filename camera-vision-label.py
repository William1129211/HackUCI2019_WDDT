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


def is_pet(pet_type, response):
    for analysis in response["responses"][0]["labelAnnotations"]:
        if analysis["description"] == pet_type:
            return True
    return False

def takephoto(count, camera):
    camera.capture('image' + str(count) + '.jpg')


def sendPhotoReceiveJSON(count, camera):
    takephoto(count, camera) # First take a picture
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
        

def main():
    cntr = 1
    camera = picamera.PiCamera()
    while(cntr < 3):
        sendPhotoReceiveJSON(cntr, camera)
        cntr += 1

    

if __name__ == '__main__':

    main()
